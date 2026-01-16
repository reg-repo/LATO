import os
import re
import subprocess

def validate_uml_with_syntax_check(uml_code, config=None):
    jar_path = None
    if config:
        jar_path = config.get_plantuml_path()
    
    if not jar_path:
        jar_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'utils', 'plantuml', 'plantuml.jar'
        )
        
    cmd = ['java', '-jar', jar_path, '-syntax']
    
    # Check if java is installed
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = proc.communicate(uml_code)
    except FileNotFoundError:
        return False, ["Java executable not found. Please install Java."]
    except Exception as e:
        return False, [f"Error running PlantUML: {e}"]

    errors = []

    # Java launch failures (e.g. wrong path)
    if err:
        for line in err.strip().splitlines():
            errors.append(f"Java/PlantUML launch error: {line}")

    # Parse PlantUML output for errors
    for line in out.splitlines():
        # Typical error lines start with "ERROR", include "Exception", or "SyntaxError"
        if re.match(r'^(ERROR|SyntaxError|Exception)', line, re.IGNORECASE):
            errors.append(line.strip())
        # Optional: capture "line X" patterns
        elif " line " in line and " :" in line:
            errors.append(line.strip())

    # Non-zero exit code but no error text
    if proc.returncode != 0 and not errors:
        errors.append(f"PlantUML exited with return code {proc.returncode} without detailed message")

    if errors:
        return False, errors
    return True, []


def extract_uml_content(text: str) -> str:
    startuml_index = text.find("@startuml")
    if startuml_index != -1:
        enduml_index = text.find("@enduml", startuml_index + len("@startuml"))
        if enduml_index != -1:
            content_start = startuml_index + len("@startuml")
            return text[content_start:enduml_index].strip()

    start_index = text.find("start\n")
    if start_index == -1:
        return text

    content_start = start_index
    end_index = text.find("@enduml", content_start)
    if end_index == -1:
        return text[content_start:].strip()
    else:
        return text[content_start:end_index].strip()


class GenerateModule:
    def __init__(self, llm, prompt_manager, config=None):
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.config = config
        
        generatePrompt = self.prompt_manager.load_prompt("generate")
        regenerate_prompt = self.prompt_manager.load_prompt("regenerate")
        
        self.generate_chain = generatePrompt | llm
        self.retry_chain = regenerate_prompt | llm

    def invoke(self, examples: str, input_data: str) -> str:
        response = self.generate_chain.invoke({
            "Examples": examples,
            "Input": input_data
        })
        uml_code = extract_uml_content(response.content)

        return self.validate_with_retry(examples, input_data, uml_code)

    def validate_with_retry(self, examples, input_data, initial_uml: str) -> str:
        current_uml = initial_uml
        count = 0
        while True:
            current_uml = extract_uml_content(current_uml)
            if count >= 5:
                return current_uml
            flag, errors = validate_uml_with_syntax_check(current_uml, self.config)

            if flag:
                return current_uml

            response = self.retry_chain.invoke({
                "Examples": examples,
                "Input": input_data,
                "errors": "\n".join(errors),
                "uml_code": current_uml
            })
            current_uml = response.content
            count += 1
