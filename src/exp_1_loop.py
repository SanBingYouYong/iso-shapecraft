from agents import visual_feedback, exp_full_task, exp_single_get_prompt, _extract_python_code, visual_feedback_get_prompts, _extract_yml_code
from chat import llm_with_history, vlm_multi_img
from combine_and_run import combine_and_run_looped
from file_utils import parse_as_yaml

import time
import os
import json
import yaml
import random
from tqdm import tqdm

'''
Initial code -> 
- error detected (in error log or syntax error): add to original dialogue with "Error encountered: ..."
- no error: show multi-view rendered images to VLM feedback agent, add feedback to original dialogue
'''

def format_feedback(feedback: str) -> str:
    return f"Please update the code based on the feedback: \n{feedback}"


def one_shape_looped(shape_description: str, exp_folder: str):
    '''
    Expects a shape description and an experiment folder (absolute path!) to output to.
    '''
    os.makedirs(exp_folder, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder) != []:
        # delete everything
        for f in os.listdir(exp_folder):
            os.remove(os.path.join(exp_folder, f))
    done = False
    max_ite = 5
    ite = 0
    history = []
    prompt = exp_single_get_prompt(shape_description)
    visual_feedbacks = []
    while not done and ite < max_ite:
        # print(f"Iteration {ite}...")
        response, history = llm_with_history(prompt, history)
        pycode = _extract_python_code(response)
        if pycode == "":
            raise ValueError("No python code extracted from LLM response.")
        pycode_path = os.path.join(exp_folder, f"{str(ite)}.py")  # use ite as basename
        with open(pycode_path, "w") as f:
            f.write(pycode)
        combine_and_run_looped(pycode_path, exp_folder)
        # check for successful execution by: stderr log's "An error occurred:" line, or {ite}_syntax_error.txt, or images exists
        syntax_error = os.path.join(exp_folder, f"{str(ite)}_syntax_error.txt")
        if os.path.exists(syntax_error):
            with open(syntax_error, "r") as f:
                error = f.read()
            prompt = f"Error encountered: {error}"
            ite += 1
            continue
        # if no syntax error, check stderr log
        error_log = os.path.join(exp_folder, f"{str(ite)}_blender_stderr.log")
        with open(error_log, "r") as f:
            error = f.read()
        if "An error occurred:" in error:
            error_lines = error.split("\n")  # skips the universal TBmalloc warning and the flag line itself
            error = error_lines[error_lines.index("An error occurred:") + 1]
            prompt = f"Error encountered: {error}"
            ite += 1
            continue
        # if no errors from above two checks, images should definitely be in place
        # find current iteration prefxied images
        images = [f for f in os.listdir(exp_folder) if f.startswith(f"{str(ite)}_") and f.endswith('.png')]
        image_paths = [os.path.join(exp_folder, img) for img in images]
        if len(images) == 0:
            raise ValueError(f"No images found for iteration {ite}.")
        for img in images:
            assert os.path.exists(os.path.join(exp_folder, img)), f"Image {img} not found."
        # visual feedback
        vis_prompt = visual_feedback_get_prompts(shape_description)
        feedback = vlm_multi_img(vis_prompt, image_paths)
        visual_feedbacks.append(
            {
                "iteration": ite,
                "prompt": vis_prompt,
                "feedback": feedback
            }
        )
        feedback_yml = _extract_yml_code(feedback)
        parsed_feedback = parse_as_yaml(feedback_yml)
        assert "issues" in parsed_feedback and "consistency" in parsed_feedback
        if parsed_feedback['consistency']:  # yaml handles parsing multiple ways of saying True already
            done = True
            # print(f"Task completed in {ite} iterations.")
        else:
            prompt = format_feedback(feedback)
            ite += 1
    # save final history
    with open(os.path.join(exp_folder, "history.json"), "w") as f:
        json.dump(history, f)
    # save visual feedbacks
    with open(os.path.join(exp_folder, "feedback.json"), "w") as f:
        json.dump(visual_feedbacks, f)
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder, "shape_description.txt"), "w") as f:
        f.write(shape_description)
    return ite, history

SHAPE_DESCRIPTIONS_YAML = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapes_daily_4omini.yaml"

def read_shapes(shapes_yaml: str) -> dict:
    with open(shapes_yaml, 'r') as stream:
        shapes = yaml.safe_load(stream)['shapes']
    return shapes

def loop_10_daily_objects():
    # sample 10 shapes
    shapes = read_shapes(SHAPE_DESCRIPTIONS_YAML)
    random.seed(0)
    selected_shapes = random.sample(shapes, 10)
    exp_out_root = os.path.abspath(f"exp\\10_looped")
    os.makedirs(exp_out_root, exist_ok=True)
    iterations = []
    for i, shape in enumerate(selected_shapes):
        timestamp = time.strftime("%m%d-%H%M%S")
        print(f"Processing shape {i}...")
        print(f"Shape description: {shape}")
        shape_out_root = os.path.join(exp_out_root, timestamp)
        print(f"Output root: {shape_out_root}")
        ite, hist = one_shape_looped(shape, shape_out_root)
        iterations.append(ite)
    with open(os.path.join(exp_out_root, "iterations.csv"), "w") as f:
        f.write("\n".join([str(i) for i in iterations]))

def all_shapes_looped(manual_skip_idx: int=0, manual_exp_out_root: str=None):
    shapes = read_shapes(SHAPE_DESCRIPTIONS_YAML)
    iterations = []
    timestamp = time.strftime("%m%d-%H%M%S")
    exp_out_root = os.path.abspath(f"exp\\single_daily_shapes_looped_all_{timestamp}") if manual_exp_out_root is None else manual_exp_out_root
    for i, shape in enumerate(tqdm(shapes)):
        if i < manual_skip_idx:  # avoid overwriting when resuming
            continue
        ite, hist = one_shape_looped(shape, os.path.join(exp_out_root, f"{str(i).zfill(4)}"))
        iterations.append(ite)
    with open(os.path.join(exp_out_root, "iterations.csv"), "w") as f:
        f.write("\n".join([str(i) for i in iterations]))

if __name__ == "__main__":
    # shape = "A chair with four legs, a backrest, no armrests, and a cushioned seat."
    # timestamp = time.strftime("%m%d-%H%M%S")
    # exp_out_root = f"exp\\looped\\{timestamp}"
    # one_shape_looped(shape, os.path.abspath(exp_out_root))

    # loop_10_daily_objects()

    # all_shapes_looped(67, os.path.abspath("exp\\single_daily_shapes_looped_all_0202-181517"))  # manual skip index for resuming
    all_shapes_looped(39, os.path.abspath("exp\\single_daily_shapes_looped_all_0202-221821"))  # manual skip index for resuming
