from langchain_openai import ChatOpenAI
import yaml
import os

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_llm_config(self, model_name):
        if model_name not in self._config:
            raise KeyError(f"Model '{model_name}' not found in configuration.")
        return self._config[model_name]

    def get_corenlp_config(self):
        return self._config.get('corenlp', {
            'host': 'http://localhost',
            'port': 9000,
            'timeout': 30000
        })

    def get_plantuml_path(self):
        return self._config.get('plantuml', {}).get('path', None)

def setup_llm(model_name, config_path):
    config = Config(config_path)
    args = config.get_llm_config(model_name)
    
    # Prioritize environment variables for keys
    api_key = os.getenv('OPENAI_API_KEY') or args.get('key')
    if not api_key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY env var or 'key' in args.yaml")

    llm = ChatOpenAI(
        temperature=args.get('temperature', 0.7),
        model=args['model'],
        openai_api_key=api_key,
        openai_api_base=args.get('base'),
    )
    
    return llm, config
