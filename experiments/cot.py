from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

prompt = ChatPromptTemplate.from_messages(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "{Examples}\n\nInput:\n{Input}\n\n"
            "Please generate PlantUML code for the activity diagram according to the above requirements.\n\n"
        )
    ]
)


class CoT:
    def __init__(self, llm, prompt_path='prompt/cot.txt'):
        self.llm = llm
        self.chain = prompt | self.llm
        # Default fallback or user provided path
        try:
            with open(prompt_path, 'r', encoding='utf-8') as file:
                self.examples = file.read()
        except FileNotFoundError:
             # If running from repo root, try different path or leave empty
             # This assumes prompt files are managed externally for these experiments
             print(f"Warning: Prompt file not found at {prompt_path}")
             self.examples = ""

    def invoke(self, data):
        response = self.chain.invoke(
            {"Examples": self.examples, "Input": data},
        )
        return response.content
