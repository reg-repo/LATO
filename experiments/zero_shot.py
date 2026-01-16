from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

prompt = ChatPromptTemplate.from_messages(
    messages=[
        HumanMessagePromptTemplate.from_template(
            "Input:\n{Input}\n\n"
            "Please generate PlantUML code for the activity diagram according to the above requirements. Output the "
            "results directly without explanation\n\n"
            "Output:"
        )
    ]
)


class ZeroShot:
    def __init__(self, llm):
        self.llm = llm
        self.chain = prompt | self.llm

    def invoke(self, data):
        response = self.chain.invoke(
            {"Input": data},
        )
        return response.content
