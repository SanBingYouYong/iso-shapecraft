from chat import llm_request, vlm_request, llm_with_history, vlm_multi_img
from prompt import read_markdown_prompts
from constants import TaskType
from file_utils import save_output, read_as_yaml, parse_as_yaml, log_output_to_exp

import yaml
import os
from typing import List, Dict
from pprint import pprint
import time

prompts = read_markdown_prompts()
with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)
config_str = f"coding language: {config['coding_language']}\nshape engine: {config['shape_engine']}\n"

def _extract_python_code(response: str) -> str:
    '''
    Extracts the python code from ```python\n<code>\n``` as str.
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

def _extract_yml_code(response: str) -> str:
    '''
    Extracts the yaml code from ```yaml\n<code>\n``` as str.
    '''
    lines = response.split('\n')
    if lines[0] == "```yml" and lines[-1] == "```":
        return '\n'.join(lines[1:-1])
    code_block = False
    code_lines = []
    for line in lines:
        if line.startswith("```yaml"):
            code_block = True
        elif code_block:
            if line.startswith("```"):
                break
            code_lines.append(line)
    return '\n'.join(code_lines)
    
def _format_issues(issues: List[Dict[str, str]]) -> str:
    formatted_str = ""
    for issue in issues:
        formatted_str += f"  - description: {issue['description']}\n    suggestion: {issue['suggestion']}\n\n"
    return formatted_str

def _format_improvement_info(description: str, code: str, feedback: List[Dict[str, str]]) -> str:
    return f"\nSub-component Shape Description: {description}\n\nExisting Code Snippet: \n{code}\n\nVisual Feedback:\n{_format_issues(feedback)}\n"

def _format_components(components: List[Dict[str, str]]) -> str:
    '''
    Formats the components dictionary into a string.
    '''
    formatted_str = ""
    for component in components:
        formatted_str += f"  - component: {component['name']}\n  - description: {component['description']}\n\n"
    return formatted_str

def format_feedback(feedback: str) -> str:
    return f"Please update the code based on the feedback: \n{feedback}"

def _extract_openscad_code(response: str) -> str:
    '''
    Extracts the openscad code from ```openscad\n<code>\n``` or ```scad\n<code>\n``` as str.
    '''
    lines = response.split('\n')
    if (lines[0] == "```openscad" or lines[0] == "```scad") and lines[-1] == "```":
        return '\n'.join(lines[1:-1])
    code_block = False
    code_lines = []
    for line in lines:
        if line.startswith("```openscad") or line.startswith("```scad"):
            code_block = True
        elif code_block:
            if line.startswith("```"):
                break
            code_lines.append(line)
    return '\n'.join(code_lines)

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

def _format_code_snippets(code_snippets: Dict[str, str]) -> str:
    '''
    Formats the code snippets dictionary into a string.
    '''
    formatted_str = ""
    for component in code_snippets:  # TODO: if testing other languages, update accordingly
        formatted_str += f"Component: {component}\n```python\n{code_snippets[component]}```\n\n"
    return formatted_str

def experiment_logger():
    '''
    Decorator to log the experiment id and task type.
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            exp_id = time.strftime("%m%d-%H%M%S")
            result = func(*args, **kwargs)
            log_output_to_exp(agents_rev[func.__name__], result, exp_id)
            return {
                "exp_id": exp_id,
                "task_type": agents_rev[func.__name__],
                "result": result
            }
        return wrapper
    return decorator

### AGENTS ###

@experiment_logger()
def exp_full_task(shape_description: str) -> Dict[str, str]:
    '''
    Experiment: zero-shot, one-run, full shape program generation based on text prompt. 
    '''
    ins = prompts[TaskType.EXP_FULL_TASK.value["name"]]
    prompt = ins + config_str + shape_description
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

def exp_single_get_prompt(shape_description: str) -> str:
    '''
    Experiment: zero-shot, one-run, full shape program generation based on text prompt. 
    '''
    ins = prompts[TaskType.EXP_FULL_TASK.value["name"]]
    return ins + config_str + shape_description

def exp_single_get_prompt_scad(shape_description: str) -> str:
    '''
    Experiment: zero-shot, one-run, full shape program generation based on text prompt. For OpenSCAD (temp)
    '''
    ins = prompts['exp_full_task_openscad']
    return ins + config_str + shape_description

def exp_full_task_batch_out(shape_description: str) -> Dict[str, str]:
    '''
    Experiment: zero-shot, one-run, full shape program generation based on text prompt. 

    For batched output folders. 
    '''
    ins = prompts[TaskType.EXP_FULL_TASK.value["name"]]
    prompt = ins + config_str + shape_description
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

@experiment_logger()
def task_decomp(shape_description: str) -> List[Dict[str, str]]:
    '''
    Prompt + user-input shape description
    '''
    ins = prompts[TaskType.TASK_DECOMP.value["name"]]
    prompt = ins + shape_description
    response = llm_request(prompt)  # this output should be in yaml format
    components = parse_as_yaml(response)["components"]
    return {
        "prompt": prompt,
        "response": response,
        "parsed": components
    }

def task_decomp_get_prompt(shape_description: str) -> str:
    '''
    Prompt + user-input shape description
    '''
    ins = prompts[TaskType.TASK_DECOMP.value["name"]]
    return ins + shape_description

# UNTESTED & Deprecated
def components_prototype(components: List[Dict[str, str]]) -> Dict[str, str]:
    '''
    tracks each component, call component synthesis and save python codes.

    To be replaced by individual pipelines.
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
# TESTED
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

def synthesize_components(components: List[Dict]) -> Dict[str, str]:
    '''
    call pipeline for all components
    '''
    comps = {}
    for component in components:
        results = individual_component_pipeline(component)
        if results["success"]:
            comps[component["name"]] = results["code"]
        else:
            print(f"Component synthesis failed for {component['name']}.")
            print(results["feedback"])
            comps[component["name"]] = "pass"  # should we abort now directly?
    return comps

# TODO: automatic rendering pipeline with Blender or OpenSCAD
def _execute_and_render(code: str, output_path: str):
    '''
    Execute the code in Blender and render the output.

    Returns image path or read image?

    Catch any bugs during execution and rendering. 
    '''
    pass

def individual_component_pipeline(component: Dict[str, str]) -> Dict[str, bool | str]:
    '''
    Pipeline for individual component synthesis: comp synth -> [vis feedback -> shape improvement]
    
    Returns dict:
        - "success": bool
        - "code": str
        - "feedback": str or ""
    '''
    done = False
    max_attempt = 3
    attempt = 0
    # initial attempt
    code = component_synth(component["name"], component["description"])["parsed"]
    while not done and attempt < max_attempt:  # TODO: maybe we use vertical logging for individual tasks and combined log for joint tasks
        image = _execute_and_render(code, f"outputs/_{component['name']}.png")
        feedback = visual_feedback(component["description"], f"outputs/_{component['name']}.png")
        if feedback["consistent"]:
            done = True
        else:
            code = shape_improvement(component["description"], code, feedback["issues"])
    return {"success": done, "code": code, "feedback": "max attempt reached"}
    
# TODO: adding a new agent to convert this output to procedural models? 
@experiment_logger()
def component_synth(name: str, description: str):
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.COMP_SYNTH.value['name']]
    prompt = ins + config_str + f"\nname: {name}\ndescription: {description}\n"
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

def component_synth_get_prompt(name: str, description: str) -> str:
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.COMP_SYNTH.value['name']]
    return ins + config_str + f"\nname: {name}\ndescription: {description}\n"

def procedural_synth(name: str, description: str):
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.PROC_SYNTH.value]
    prompt = ins + config_str + f"\nname: {name}\ndescription: {description}\n"
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

def procedural_synth_get_prompt(name: str, description: str) -> str:
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.PROC_SYNTH.value]
    return ins + config_str + f"\nname: {name}\ndescription: {description}\n"

@experiment_logger()
def visual_feedback(shape_description: str, image_path: str) -> dict:
    '''
    Prompt + shape description + image
    TODO: may need multi-view rendering (e.g. front, side, top) for consistent feedback

    Returns dict: issues(list of dict), consistent(bool)
        issues: 
        - description: [issue description]
          suggestion: [suggestion to correct or improve]
        - ...
        consistenct: [true/false based on the significance of identified issues]
    '''
    ins = prompts[TaskType.VIS_FEEDBACK.value]
    prompt = ins + shape_description
    response = vlm_request(prompt, image_path)  # this output should be in yaml format
    feedback = parse_as_yaml(response)["feedback"]
    return {
        "prompt": prompt,
        "response": response,
        "parsed": feedback
    }

def visual_feedback_get_prompts(shape_description: str) -> str:
    '''
    Prompt + shape description
    '''
    ins = prompts[TaskType.VIS_FEEDBACK.value]
    return ins + shape_description

@experiment_logger()
def shape_improvement(shape_description: str, original_code: str, feedback: List[Dict[str, str]]):
    '''
    Prompt + shape description + original code + feedback

    feedback: issues {description:suggestion}
    '''
    ins = prompts[TaskType.SHAPE_IMPROVEMENT.value]
    prompt = ins + _format_improvement_info(shape_description, original_code, feedback)
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

# TODO: maybe we can combine this task into decomposition agent? or is it the same thing just longer context
@experiment_logger()
def high_level_aggregation(user_input: str, components: List[Dict[str, str]]):
    '''
    Prompt + user-input + components (name and descriptions)
    
    Returns as str, high-level instructions for code aggregation.
    '''
    ins = prompts[TaskType.HIGH_AGGRE.value]
    prompt = ins + f"\nUser Prompt: {user_input}\n\nSub-components:\n{_format_components(components)}\n"
    response = llm_request(prompt)  # this output should be in plain text
    return {
        "prompt": prompt,
        "response": response,
        "parsed": response
    }

def high_level_aggregation_get_prompt(user_input: str, components: List[Dict[str, str]]) -> str:
    '''
    Prompt + user-input + components (name and descriptions)
    '''
    ins = prompts[TaskType.HIGH_AGGRE.value]
    return ins + f"\nUser Prompt: {user_input}\n\nSub-components:\n{_format_components(components)}\n"

# TODO: this can be on putting mesh together directly, like scenecraft with new assets
@experiment_logger()
def code_level_aggregation(high_level_instruct: str, code_snippets: Dict[str, str]):
    '''
    Prompt + high-level instructions + code snippets {component name: code}
    
    returns python code in str.
    '''
    ins = prompts[TaskType.CODE_AGGRE.value]
    prompt = ins + f"\nHigh-level Aggregation Instructions: {high_level_instruct}\n\nCode Snippets:\n{_format_code_snippets(code_snippets)}\n"
    response = llm_request(prompt)  # this output should be python code wrapped in markdown code block
    pycode = _extract_python_code(response)
    return {
        "prompt": prompt,
        "response": response,
        "parsed": pycode
    }

def code_level_aggregation_get_prompt(high_level_instruct: str, code_snippets: Dict[str, str]) -> str:
    '''
    Prompt + high-level instructions + code snippets {component name: code}
    '''
    ins = prompts[TaskType.CODE_AGGRE.value]
    return ins + f"\nHigh-level Aggregation Instructions: {high_level_instruct}\n\nCode Snippets:\n{_format_code_snippets(code_snippets)}\n"

def shape_evaluation(shape_description: str, image_paths: List[str]) -> dict:
    '''
    Prompt + shape description + images
    '''
    ins = prompts[TaskType.SHAPE_EVALUATION.value]
    prompt = ins + shape_description
    response = vlm_multi_img(prompt, image_paths)  # this output should be in yaml format
    feedback = _extract_yml_code(response)
    try:
        feedback = parse_as_yaml(feedback)
        assert 'score' in feedback and 'explanation' in feedback, f"Feedback not in expected format: {feedback}"
    except Exception as e:
        print(f"Error in parsing feedback: {e}")
        feedback = {"score": 0, "explanation": "Feedback parsing error. Here's the original feedback:\n" + feedback}
    return {
        "prompt": prompt,
        "response": response,
        "parsed": feedback
    }

agents = {
    TaskType.TASK_DECOMP: task_decomp,
    TaskType.COMP_SYNTH: component_synth,
    TaskType.PROC_SYNTH: procedural_synth,
    TaskType.VIS_FEEDBACK: visual_feedback,
    TaskType.SHAPE_IMPROVEMENT: shape_improvement,
    TaskType.HIGH_AGGRE: high_level_aggregation,
    TaskType.CODE_AGGRE: code_level_aggregation,
    TaskType.SHAPE_EVALUATION: shape_evaluation
}
agents_rev = {
    "task_decomp": TaskType.TASK_DECOMP,
    "component_synth": TaskType.COMP_SYNTH,
    "procedural_synth": TaskType.PROC_SYNTH,
    "visual_feedback": TaskType.VIS_FEEDBACK,
    "shape_improvement": TaskType.SHAPE_IMPROVEMENT,
    "shape_evaluation": TaskType.SHAPE_EVALUATION,
    "high_level_aggregation": TaskType.HIGH_AGGRE,
    "code_level_aggregation": TaskType.CODE_AGGRE,
    "exp_full_task": TaskType.EXP_FULL_TASK
}

if __name__ == "__main__":
    # shape_description = "An upright, rectangular shape that connects to the rear of the chair seat. It should be taller than the seat and have a slight incline for ergonomic support. The edges can be rounded to match the style of the seat."
    # shape_description = "A chair with four legs, a seat, and a backrest. The legs should be sturdy and slightly angled outwards for stability. The seat should be flat and comfortable, and the backrest should be slightly curved to provide ergonomic support."
    # pycode = exp_full_task(shape_description)["parsed"]

    # print(_extract_python_code("") == "")

    image_paths = "0_0.png", "0_1.png", "0_2.png", "0_3.png"
    image_paths = [os.path.join("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\\full\\chair\\aggregator", img) for img in image_paths]
    shape_description = "a chair"
    feedback = shape_evaluation(shape_description, image_paths)["parsed"]
    print(feedback)
    
    # components = task_decomp(shape_description)["parsed"]
    # test_comp = components[0]
    # pycode = component_synth(test_comp["name"], test_comp["description"])["parsed"]
    
    # prompt, response = task_decomp(shape_description)
    # components = read_as_yaml("outputs/0_task_decomposition.txt")["components"]
    # # code_snippets = components_wrapper(components['components'])
    # code_snippets = _gather_code_snippets()
    # high_level_prompt, high_level_response = high_level_aggregation(shape_description, components)
    # code_level_prompt, code_level_response = code_level_aggregation(high_level_response, code_snippets)
    # # to be integrated into wrapper like comps wrapper
    # final_python = _extract_python_code(high_level_response)
    # with open("outputs/_final_python.py", "w") as file:
    #     file.write(final_python)
    # print(code_level_response)

