from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

prompt = ChatPromptTemplate.from_messages(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "{Examples}\n\nInput:\n{Input}\n\n"
            "Please generate the PlantUML code for the activity diagram based on the above requirements. Output the "
            "result directly without explanation.\n\n"
            "Output:"
        )
    ]
)


class FewShot:
    def __init__(self, llm, prompt_path='prompt/few.txt'):
        self.llm = llm
        self.chain = prompt | self.llm
        try:
            with open(prompt_path, 'r', encoding='utf-8') as file:
                self.examples = file.read()
        except FileNotFoundError:
             print(f"Warning: Prompt file not found at {prompt_path}")
             self.examples = ""

    def invoke(self, data):
        response = self.chain.invoke(
            {"Examples": self.examples, "Input": data},
        )
        return response.content
