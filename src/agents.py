from chat import llm_request, vlm_request
from prompt import read_markdown_prompts
from constants import TaskType

import yaml
import os

prompts = read_markdown_prompts()
with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)
config_str = f"coding language: {config['coding_language']}\nshape engine: {config['shape_engine']}\n"

def _save_output(task_type: TaskType, response: str) -> None:
    with open(f"outputs/{task_type.value}.txt", "w") as file:
        file.write(response)

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

def task_decomp(user_input: str) -> str:
    '''
    Prompt + user-input shape description
    '''
    ins = prompts[TaskType.TASK_DECOMP.value]
    prompt = ins + user_input
    response = llm_request(prompt)
    _save_output(TaskType.TASK_DECOMP, response)
    return prompt, response

# TODO: for unit-testing; for real pipeline we need to track each task dynamically and save/run outputs accordingly
def component_synth(shape_description: str):
    '''
    Prompt + config (coding language + shape engine) + shape description
    '''
    ins = prompts[TaskType.COMP_SYNTH.value]
    prompt = ins + config_str + "description: " + shape_description
    response = llm_request(prompt)
    _save_output(TaskType.COMP_SYNTH, response)
    return prompt, response

# TODO: may need multi-view rendering (e.g. front, side, top) for consistent feedback
def visual_feedback(shape_description: str, image_path: str):
    '''
    Prompt + shape description + image
    '''
    ins = prompts[TaskType.VIS_FEEDBACK.value]
    prompt = ins + shape_description
    response = vlm_request(prompt, image_path)
    _save_output(TaskType.VIS_FEEDBACK, response)
    return prompt, response

def shape_improvement(shape_description: str, original_code: str, feedback: str):
    '''
    Prompt + shape description + original code + feedback
    '''
    ins = prompts[TaskType.SHAPE_IMPROVEMENT.value]
    prompt = ins + _format_improvement_info(shape_description, original_code, feedback)
    response = llm_request(prompt)
    _save_output(TaskType.SHAPE_IMPROVEMENT, response)
    return prompt, response

if __name__ == "__main__":
    shape_description = "An upright, rectangular shape that connects to the rear of the chair seat. It should be taller than the seat and have a slight incline for ergonomic support. The edges can be rounded to match the style of the seat."
    with open("outputs/1_component_synthesis.txt", "r") as f:
        code = f.read()
    with open("outputs/1_visual_feedback.txt", "r") as f:
        feedback = f.read()
    prompt, response = shape_improvement(shape_description, code, feedback)
    print(prompt)
    print(response)

