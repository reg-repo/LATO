from fastcoref import FCoref
from langgraph.graph import StateGraph, END
import torch

def get_max_calibrate_rounds(input_data):
    length = len(input_data)
    if length < 200:
        return 3
    elif length < 800:
        return 6
    else:
        return 8

class IdentifyModule:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager
        # Auto-detect device
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model = FCoref(device=device)
        self._build_graph()

    def _build_graph(self):
        # Load prompts via manager
        identifyPrompt = self.prompt_manager.load_prompt("identify")
        calibratePrompt = self.prompt_manager.load_prompt("calibrate")

        def identify_node(state):
            chain = identifyPrompt | self.llm
            res = chain.invoke({"Examples": state['examples'], "Input": state['input_data']})
            new_state = dict(state)
            new_state.update({
                "last_output": res.content
            })
            return new_state

        def coref_node(state):
            coref_result = self.model.predict(texts=[state['input_data']])
            new_state = dict(state)
            new_state.update({
                "coref_result": coref_result
            })
            return new_state

        def calibrate_node(state):
            calibrator = calibratePrompt | self.llm
            count = state.get('calibrate_count', 0) + 1
            prev_output = state.get('prev_output', None)
            res = calibrator.invoke({
                "Examples": state['examples'],
                "Input": state['input_data'],
                "Output": state['last_output'],
                "CoreF": state['coref_result'],
            }).content
            max_rounds = get_max_calibrate_rounds(state['input_data'])
            new_state = dict(state)
            if '[OK]' in res or count >= max_rounds or res == prev_output:
                new_state.update({
                    "final_result": state['last_output'],
                    "calibrate_count": count,
                    "done": True
                })
            else:
                new_state.update({
                    "last_output": res,
                    "calibrate_count": count,
                    "prev_output": state['last_output'],
                    "done": False
                })
            return new_state

        graph = StateGraph(dict)
        graph.add_node("identify", identify_node)
        graph.add_node("coref", coref_node)
        graph.add_node("calibrate", calibrate_node)
        graph.add_edge("identify", "coref")
        graph.add_edge("coref", "calibrate")
        graph.add_conditional_edges(
            "calibrate",
            lambda state: END if state.get("done") else "calibrate"
        )
        graph.set_entry_point("identify")
        self.identify_graph = graph.compile()

    def invoke(self, examples, data):
        state = {
            "llm": self.llm,
            "examples": examples,
            "input_data": data,
            "last_output": None,
            "calibrate_count": 0,
            "prev_output": None
        }
        result = self.identify_graph.invoke(state)
        return result.get("final_result")
