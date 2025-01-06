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


if __name__ == "__main__":
    shape_description = "An upright, rectangular shape that connects to the rear of the chair seat. It should be taller than the seat and have a slight incline for ergonomic support. The edges can be rounded to match the style of the seat."
    prompt, response = visual_feedback(shape_description, "test.png")
    print(prompt)
    print(response)

