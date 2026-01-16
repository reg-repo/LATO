import json
from stanfordcorenlp import StanfordCoreNLP
from langgraph.graph import StateGraph, END

def getTree(data, host='http://localhost', port=9000, timeout=30000):
    depend_tree = ''
    try:
        with StanfordCoreNLP(host, port=port, timeout=timeout) as nlp:
            props = {
                'annotators': 'tokenize,ssplit,pos,depparse',
                'outputFormat': 'json'
            }
            try:
                ann = nlp.annotate(data, properties=props)
                j = json.loads(ann)
                dependencies = j['sentences'][0]['basicDependencies']
                tokens = j['sentences'][0]['tokens']
                words = [token['word'] + '-' + str(token['index'] - 1) for token in tokens]
                dependencies.sort(key=lambda arc: arc['dependent'])
                relations = [arc['dep'] for arc in dependencies]
                rely_ids = [arc['governor'] for arc in dependencies]
                heads = ['Root' if gid == 0 else words[gid - 1] for gid in rely_ids]
                for i in range(len(words)):
                    depend_tree += f"{relations[i]}({words[i]}, {heads[i]})\n"
            except json.JSONDecodeError:
                print("Error: Server response is not valid JSON. Is the CoreNLP server running and reachable?")
            except Exception as e:
                print(f"Error processing data with CoreNLP: {e}")
    except Exception as e:
         print(f"Error connecting to CoreNLP server at {host}:{port}: {e}")
         return ""
         
    return depend_tree

class DecomposeModule:
    def __init__(self, llm, prompt_manager, config=None, max_retry=5, max_level=10):
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.config = config
        self.max_retry = max_retry
        self.max_level = max_level
        self._build_graph()

    def _build_graph(self):
        # Load prompts
        decomposePrompt = self.prompt_manager.load_prompt("decompose")
        verifyPrompt = self.prompt_manager.load_prompt("verify")
        
        self.executor = decomposePrompt | self.llm
        self.verifier = verifyPrompt | self.llm

        def dependency_tree_node(state):
            corenlp_config = {}
            if self.config:
                corenlp_config = self.config.get_corenlp_config()
            
            depend_tree = getTree(
                state['input_data'], 
                host=corenlp_config.get('host', 'http://localhost'),
                port=corenlp_config.get('port', 9000),
                timeout=corenlp_config.get('timeout', 30000)
            )
            return {**state, 'depend_tree': depend_tree}

        def decompose_node(state):
            execution = self.executor.invoke(
                {
                    "Examples": state['examples'],
                    "Input": state['input_data'],
                    "FormerOutput": state.get('former_output', '') + state.get('last_check', ''),
                    "Level": state['level']
                }
            ).content
            return {**state, 'execution': execution}

        def verify_node(state):
            verification = self.verifier.invoke(
                {
                    "Examples": state['examples'],
                    "Input": state['input_data'],
                    "FormerOutput": state.get('former_output', ''),
                    "Output": state['execution'],
                    "Depend": state['depend_tree']
                }
            ).content
            former_output = state.get('former_output', '')
            level = state['level']
            count = state.get('count', 0) + 1
            last_check = '\n' + verification

            if "[Valid]" in verification:
                former_output += state['execution'] + '\n'
                level += 1
                count = 1

                if level > self.max_level:
                    return {
                        **state, 
                        'final_result': former_output + f"\n[Terminated: exceed max_level {self.max_level}]", 
                        'done': True
                    }

                if '[' not in state['execution'] and ']' not in state['execution']:
                    return {**state, 'final_result': former_output, 'done': True}

                return {
                    **state,
                    'former_output': former_output,
                    'last_check': '',
                    'level': level,
                    'count': 1,
                    'done': False
                }

            if count >= self.max_retry:
                return {
                    **state,
                    'final_result': former_output + f"\n[Terminated at level {level} after {self.max_retry} retries. Last check: {verification}]",
                    'done': True
                }

            return {
                **state,
                'last_check': last_check,
                'count': count,
                'done': False
            }

        graph = StateGraph(dict)
        graph.add_node("dependency_tree", dependency_tree_node)
        graph.add_node("decompose", decompose_node)
        graph.add_node("verify", verify_node)
        graph.add_edge("dependency_tree", "decompose")
        graph.add_edge("decompose", "verify")
        graph.add_conditional_edges(
            "verify",
            lambda state: END if state.get("done") else "decompose"
        )
        graph.set_entry_point("dependency_tree")
        self.decompose_graph = graph.compile()

    def invoke(self, examples, data):
        recursion_limit = (self.max_level * self.max_retry) + 20
        state = {
            "examples": examples,
            "input_data": data,
            "former_output": '',
            "last_check": '',
            "level": 1,
            "count": 0
        }
        
        result = self.decompose_graph.invoke(
            state, 
            config={"recursion_limit": recursion_limit}
        )
        return result.get('final_result')
