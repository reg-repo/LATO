from src.modules.identify import IdentifyModule
from src.modules.extract import DecomposeModule
from src.modules.construct import GenerateModule
from src.modules.integrate import ReconstructModule
from src.utils.prompt_manager import PromptManager
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("LATO")

class LATO:
    """
    LATO: Layerwise Analysis-driven auTomatic behavioral mOdeling
    
    This class orchestrates the LATO workflow:
    1. Identification: Identify atomic activities.
    2. Decomposition: Extract relations and structures.
    3. Reconstruction: Integrate information into a structured format.
    4. Generation: Generate the final PlantUML code.
    """
    def __init__(self, llm, config=None):
        # Initialize PromptManager
        prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
        self.prompt_manager = PromptManager(prompts_dir)
        
        self.identification = IdentifyModule(llm, self.prompt_manager)
        self.decomposition = DecomposeModule(llm, self.prompt_manager, config=config)
        self.reconstruction = ReconstructModule(llm, self.prompt_manager)
        self.generation = GenerateModule(llm, self.prompt_manager, config=config)

    def workflow(self, input_data, examples_path):
        if not os.path.isdir(examples_path):
             raise FileNotFoundError(f"Examples directory not found: {examples_path}")

        # Helper to read example files safely
        def read_example(filename):
            path = os.path.join(examples_path, filename)
            if not os.path.exists(path):
                 raise FileNotFoundError(f"Example file not found: {path}")
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()

        # identifier
        logger.info("START: Activity Identification")
        identify_examples = read_example('identify.txt')
        identify_result = '#Activity Identification\n' + self.identification.invoke(identify_examples, input_data)
        logger.info("END: Activity Identification")

        # extractor
        logger.info("START: Relation Decomposition")
        decompose_examples = read_example('decompose.txt')
        decompose_input = input_data + '\n\n'
        decompose_result = '#Relation Decomposition\n' + self.decomposition.invoke(decompose_examples, decompose_input)
        logger.info("END: Relation Decomposition")

        # constructor (Integration)
        logger.info("START: Information Integration")
        analyze_examples = read_example('reconstruct.txt')
        analyze_input = input_data + '\n\n' + identify_result + '\n\n' + decompose_result + '\n\n'
        analyze_result = '#Information Integration\n' + self.reconstruction.invoke(analyze_examples, analyze_input)
        logger.info("END: Information Integration")

        # generator
        logger.info("START: Generation")
        generate_examples = read_example('generate.txt')
        generate_input = input_data + '\n\n' + analyze_result + '\n\n'
        generate_result = self.generation.invoke(generate_examples, generate_input)
        logger.info("END: Generation")

        return generate_result
