class ReconstructModule:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager
        reconstructPrompt = self.prompt_manager.load_prompt("reconstruct")
        self.chain = reconstructPrompt | self.llm

    def invoke(self, examples, data):
        response = self.chain.invoke(
            {"Examples": examples, "Input": data},
        )
        return response.content
