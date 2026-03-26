import json
import os
import logging
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, prompts_dir):
        self.prompts_dir = prompts_dir
        self._prompts = {}

    def load_prompt(self, prompt_name):
        if prompt_name in self._prompts:
            return self._prompts[prompt_name]

        file_path = os.path.join(self.prompts_dir, f"{prompt_name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        messages = []
        if "system" in data:
            messages.append(SystemMessagePromptTemplate.from_template(data["system"]))
        
        if "human" in data:
            messages.append(HumanMessagePromptTemplate.from_template(data["human"]))
        
        # Support for list of messages if needed in future
        if "messages" in data:
            for msg in data["messages"]:
                if msg["role"] == "system":
                    messages.append(SystemMessagePromptTemplate.from_template(msg["content"]))
                elif msg["role"] == "user":
                    messages.append(HumanMessagePromptTemplate.from_template(msg["content"]))

        prompt_template = ChatPromptTemplate.from_messages(messages)
        self._prompts[prompt_name] = prompt_template
        logger.debug(f"Loaded prompt: {prompt_name}")
        return prompt_template
