from chat import llm_request, vlm_request
from prompt import read_markdown_prompts
from constants import TaskType

import yaml
import os
from pprint import pprint

prompts = read_markdown_prompts()
with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)
config_str = f"coding language: {config['coding_language']}\nshape engine: {config['shape_engine']}\n"

def _save_output(task_type: TaskType, response: str) -> None:
    with open(f"outputs/{task_type.value}.txt", "w") as file:
        file.write(response)

def _read_as_yaml(file_path: str) -> dict:
    '''
    Reads a plain text file as a yaml file.

    Error handling: let it crash.
    '''
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def _extract_python_code(response: str) -> str:
    '''
    Extracts the python code from ```python\n<code>\n```.
    '''
    lines = response.split('\n')
    if lines[0] == "```python" and lines[-1] == "```":
        return '\n'.join(lines[1:-1])
    code_block = False
    code_lines = []
    for line in lines:
        if line.startswith("```python"):
            code_block = True
        elif code_block:
            if line.startswith("```"):
                break
            code_lines.append(line)
    return '\n'.join(code_lines)
    

def _clean_feedback(feedback: str) -> str:
    '''
    Removes the decision line on consistency from the feedback.
    '''
    lines = feedback.split('\n')
    end_with_decision = lambda line: line.endswith("Yes") or line.endswith("No") or line.endswith("yes") or line.endswith("no")
    consistency_line = lambda line: "Consistency" in line and end_with_decision(line)
    cleaned_lines = [line for line in lines if line.strip() and not consistency_line(line)]
    return '\n'.join(cleaned_lines)

def _format_improvement_info(description: str, code: str, feedback: str) -> str:
    return f"\nSub-component Shape Description: {description}\n\nExisting Code Snippet: \n{code}\n\nVisual Feedback:\n{_clean_feedback(feedback)}\n"

def _format_components(components: list) -> str:
    '''
    Formats the components dictionary into a string.
    '''
    formatted_str = ""
    for component in components:
        formatted_str += f"  - component: {component['name']}\n  - description: {component['description']}\n\n"
    return formatted_str

def _format_high_level_aggregation(user_input: str, components: list) -> str:
    return f"\nUser Prompt: {user_input}\n\nSub-components:\n{_format_components(components)}\n"

def _gather_code_snippets(folder: str="outputs") -> dict:
    '''
    Gathers all code snippets from the outputs folder.
    '''
    code_snippets = {}
    for filename in os.listdir(folder):
        if filename.endswith(".py") and filename.startswith("_"):
            cleaned_filename = filename[1:-3]
            with open(os.path.join(folder, filename), "r") as file:
                code_snippets[cleaned_filename] = file.read()
    return code_snippets

def _format_code_snippets(code_snippets: dict) -> str:
    '''
    Formats the code snippets dictionary into a string.
    '''
    formatted_str = ""
    for component in code_snippets:
        formatted_str += f"Component: {component}\n```python{code_snippets[component]}```\n\n"
    return formatted_str

### AGENTS ###

def task_decomp(user_input: str) -> str:
    '''
    Prompt + user-input shape description
    '''
    ins = prompts[TaskType.TASK_DECOMP.value]
    prompt = ins + user_input
    response = llm_request(prompt)  # this output should be in yaml format
    _save_output(TaskType.TASK_DECOMP, response)
    return prompt, response

# UNTESTED
def components_wrapper(components: list) -> dict:
    '''
    tracks each component, call component synthesis and save python codes.
    '''
    # component_responses = {}
    code_snippets = {}
    for component in components:
        prompt, response = component_synth(component['name'], component['description'])
        # component_responses[component['name']] = response
        python_code = _extract_python_code(response)
        code_snippets[component['name']] = python_code
        with open(f"outputs/_{component['name']}.py", "w") as file:
            file.write(python_code)
    return code_snippets
    # component_responses = {}
    # for component in components:
    #     prompt, response = component_synth(component['name'], component['description'])
    #     component_responses[component['name']] = response
    # code_snippets = {}
    # for comp_resp in component_responses:
    #     python_code = _extract_python_code(component_responses[comp_resp])
    #     code_snippets[comp_resp] = python_code
    #     with open(f"outputs/_{comp_resp}.py", "w") as file:
    #         file.write(python_code)
    # return code_snippets

def component_synth(name: str, description: str):
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.COMP_SYNTH.value]
    prompt = ins + config_str + f"\nname: {name}\ndescription: {description}\n"
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    _save_output(TaskType.COMP_SYNTH, response)
    return prompt, response

# TODO: may need multi-view rendering (e.g. front, side, top) for consistent feedback
def visual_feedback(shape_description: str, image_path: str):
    '''
    Prompt + shape description + image
    '''
    ins = prompts[TaskType.VIS_FEEDBACK.value]
    prompt = ins + shape_description
    response = vlm_request(prompt, image_path)  # this output should be in yaml format
    _save_output(TaskType.VIS_FEEDBACK, response)
    return prompt, response

def shape_improvement(shape_description: str, original_code: str, feedback: str):
    '''
    Prompt + shape description + original code + feedback
    '''
    ins = prompts[TaskType.SHAPE_IMPROVEMENT.value]
    prompt = ins + _format_improvement_info(shape_description, original_code, feedback)
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    _save_output(TaskType.SHAPE_IMPROVEMENT, response)
    return prompt, response

def high_level_aggregation(user_input: str, components: str):
    '''
    Prompt + user-input + components
    '''
    ins = prompts[TaskType.HIGH_AGGRE.value]
    prompt = ins + _format_high_level_aggregation(user_input, components)
    response = llm_request(prompt)  # this output should be in plain text
    _save_output(TaskType.HIGH_AGGRE, response)
    return prompt, response

def code_level_aggregation(high_level_instruct: str, code_snippets: dict):
    '''
    Prompt + high-level instructions + code snippets
    '''
    ins = prompts[TaskType.CODE_AGGRE.value]
    prompt = ins + f"\nHigh-level Instructions: {high_level_instruct}\n\nCode Snippets:\n{_format_code_snippets(code_snippets)}\n"
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    _save_output(TaskType.CODE_AGGRE, response)
    return prompt, response

if __name__ == "__main__":
    shape_description = "An upright, rectangular shape that connects to the rear of the chair seat. It should be taller than the seat and have a slight incline for ergonomic support. The edges can be rounded to match the style of the seat."
    # prompt, response = task_decomp(shape_description)
    components = _read_as_yaml("outputs/0_task_decomposition.txt")["components"]
    # code_snippets = components_wrapper(components['components'])
    code_snippets = _gather_code_snippets()
    high_level_prompt, high_level_response = high_level_aggregation(shape_description, components)
    code_level_prompt, code_level_response = code_level_aggregation(high_level_response, code_snippets)
    # to be integrated into wrapper like comps wrapper
    final_python = _extract_python_code(high_level_response)
    with open("outputs/_final_python.py", "w") as file:
        file.write(final_python)
    print(code_level_response)

