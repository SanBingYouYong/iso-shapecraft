from openscad_utils import run_openscad, run_render_export
from agents import llm_with_history, exp_single_get_prompt_scad, _extract_openscad_code, shape_evaluation, format_feedback, one_issue

import os
import json
import yaml
from tqdm import tqdm
import random

with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)
PATHS = config["paths"]
PATH_MAX_ITER = config["path_max_iter"]


def one_shape_mp_eaf(shape_description: str, exp_folder_abs: str, paths=PATHS, path_max_iter=PATH_MAX_ITER):
    '''
    Expects a shape description and an experiment folder (absolute path!) to output to.
    
    foreach path foreach iteration, if execution successful then run evaluation and store results

    now uses evaluation directly as feedback
    '''
    os.makedirs(exp_folder_abs, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder_abs) != []:
        # delete everything
        for f in os.listdir(exp_folder_abs):
            os.remove(os.path.join(exp_folder_abs, f))
    evaluation_prompt_record = None
    evaluation_history = []
    done = False
    evaluations = []
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, f"shape_description.txt"), "w") as f:
        f.write(shape_description)
    for path in range(paths):
        if done:
            break
        # print(f"Processing path {path}...")
        ite = 0
        history = []
        prompt = exp_single_get_prompt_scad(shape_description)
        while not done and ite < path_max_iter:
            # print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            scad_code = _extract_openscad_code(response)
            if scad_code == "":
                raise ValueError(f"No OpenSCAD code extracted from LLM response. {response}")
            scad_code_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.scad")
            with open(scad_code_path, "w") as f:
                f.write(scad_code)
            # run_openscad(scad_code_path, exp_folder_abs)
            run_render_export(scad_code_path, exp_folder_abs)
            # check for successful execution
            error_log_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.log")
            if os.path.exists(error_log_path):
                with open(error_log_path, "r") as error_log:
                    errors = error_log.read()
                if errors:
                    error_lines = errors.split("\n")
                    errors = "\n".join([f" - {line}" for line in error_lines if line])
                    prompt = f"Error during execution:\n{errors}"
                    ite += 1
                    continue
            # if no errors from above two checks, images should definitely be in place (openscad plan to render one image for now)
            images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(path)}_{str(ite)}_") and f.endswith('.png')]
            image_paths = [os.path.join(exp_folder_abs, img) for img in images]
            if len(images) == 0:
                raise ValueError(f"No images found for iteration {ite}, path {path} at {exp_folder_abs}.")
            for img in images:
                assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
            # evaluation
            eval_result = shape_evaluation(shape_description, image_paths)
            # print(f"Evaluation result: {eval_result['parsed']}")
            if evaluation_prompt_record is None:
                evaluation_prompt_record = eval_result['prompt']
            evaluation_history.append(
                {
                    "path": path,
                    "iteration": ite,
                    "evaluation_response": eval_result['response'],
                }
            )
            score = eval_result['parsed']['score']
            evaluations.append(
                (score, scad_code_path)
            )
            feedback = eval_result['parsed']['explanation']
            prompt = format_feedback(feedback)
            ite += 1
            if int(score) >= 9:
                done = True
        # save final history
        with open(os.path.join(exp_folder_abs, f"{str(path)}_history.json"), "w") as f:
            json.dump(history, f)
    # save evaluation history
    with open(os.path.join(exp_folder_abs, f"evaluation_history.json"), "w") as f:
        json.dump(evaluation_history, f)
    # save evaluations
    with open(os.path.join(exp_folder_abs, f"evaluations.json"), "w") as f:
        json.dump(evaluations, f)
    # save evaluation prompt used
    with open(os.path.join(exp_folder_abs, f"evaluation_prompt.md"), "w") as f:
        f.write(evaluation_prompt_record)
    # choose best
    best_score, best_code_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_code_path": best_code_path,
    }

# EVAL: tested 10 daily
def one_shape_mp_one_issue(shape_description: str, exp_folder_abs: str, paths=PATHS, path_max_iter=PATH_MAX_ITER):
    '''
    Expects a shape description and an experiment folder (absolute path!) to output to.
    
    foreach path foreach iteration, if execution successful then run evaluation and store results

    now uses evaluation directly as feedback
    '''
    os.makedirs(exp_folder_abs, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder_abs) != []:
        # delete everything
        for f in os.listdir(exp_folder_abs):
            os.remove(os.path.join(exp_folder_abs, f))
    evaluation_prompt_record = None
    evaluation_history = []
    done = False
    evaluations = []
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, f"shape_description.txt"), "w") as f:
        f.write(shape_description)
    for path in range(paths):
        if done:
            break
        # print(f"Processing path {path}...")
        ite = 0
        history = []
        prompt = exp_single_get_prompt_scad(shape_description)
        while not done and ite < path_max_iter:
            # print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            scad_code = _extract_openscad_code(response)
            if scad_code == "":
                raise ValueError(f"No OpenSCAD code extracted from LLM response. {response}")
            scad_code_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.scad")
            with open(scad_code_path, "w") as f:
                f.write(scad_code)
            # run_openscad(scad_code_path, exp_folder_abs)
            run_render_export(scad_code_path, exp_folder_abs)
            # check for successful execution
            error_log_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.log")
            if os.path.exists(error_log_path):
                with open(error_log_path, "r") as error_log:
                    errors = error_log.read()
                if errors:
                    error_lines = errors.split("\n")
                    errors = "\n".join([f" - {line}" for line in error_lines if line])
                    prompt = f"Error during execution:\n{errors}"
                    ite += 1
                    continue
            # if no errors from above two checks, images should definitely be in place (openscad plan to render one image for now)
            images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(path)}_{str(ite)}_") and f.endswith('.png')]
            image_paths = [os.path.join(exp_folder_abs, img) for img in images]
            if len(images) == 0:
                raise ValueError(f"No images found for iteration {ite}, path {path} at {exp_folder_abs}.")
            for img in images:
                assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
            # visual feedback
            one_issue_feedback = one_issue(shape_description, image_paths)['response']  # this is not recorded, but its content will appear in main history
            prompt = format_feedback(one_issue_feedback)
            # evaluation
            eval_result = shape_evaluation(shape_description, image_paths)
            # print(f"Evaluation result: {eval_result['parsed']}")
            if evaluation_prompt_record is None:
                evaluation_prompt_record = eval_result['prompt']
            evaluation_history.append(
                {
                    "path": path,
                    "iteration": ite,
                    "evaluation_response": eval_result['response'],
                }
            )
            score = eval_result['parsed']['score']
            evaluations.append(
                (score, scad_code_path)
            )
            ite += 1
            if int(score) >= 9:
                done = True
        # save final history
        with open(os.path.join(exp_folder_abs, f"{str(path)}_history.json"), "w") as f:
            json.dump(history, f)
    # save evaluation history
    with open(os.path.join(exp_folder_abs, f"evaluation_history.json"), "w") as f:
        json.dump(evaluation_history, f)
    # save evaluations
    with open(os.path.join(exp_folder_abs, f"evaluations.json"), "w") as f:
        json.dump(evaluations, f)
    # save evaluation prompt used
    with open(os.path.join(exp_folder_abs, f"evaluation_prompt.md"), "w") as f:
        f.write(evaluation_prompt_record)
    # choose best
    best_score, best_code_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_code_path": best_code_path,
    }

def for_n_shapes(data_yml: str, n: int=3, sample=False):
    '''
    data_yml: str (absolute path)
    n: int
    '''
    with open(data_yml, "r") as f:
        data = yaml.safe_load(f)['shapes']
    if sample:
        data = random.sample(data, min(n, len(data)))
    else:
        if len(data) < n:
            n = len(data)
        data = data[:n]
    exp_root = f"eval_scad_single_{n}x_{os.path.basename(data_yml).split('.')[0]}"
    for i in tqdm(range(len(data)), desc="Processing shapes"):
        shape_description = data[i]
        exp_folder_abs = os.path.abspath(os.path.join("exp", exp_root, f"shape_{i:04d}"))
        result = one_shape_mp_one_issue(shape_description, exp_folder_abs)
    print("Operation completed successfully.")


if __name__ == "__main__":
    # shape_description = "A cylindrical coffee mug with a handle on the side."
    # exp_folder_abs = os.path.abspath(os.path.join("exp", "manual", "coffee_mug_os2"))
    # # result = one_shape_mp_eaf(shape_description, exp_folder_abs)
    # result = one_shape_mp_eaf_one_issue(shape_description, exp_folder_abs)
    # print(result)
    # print("Operation completed successfully.")

    random.seed(0)

    # data_yml = "dataset/shapes_daily_multistruct_4omini.yaml"
    # data_yml = "dataset/shapes_simple_4omini.yaml"
    # data_yml = "dataset/shapes_daily_4omini.yaml"
    data_yml = "dataset/shapes_primitive_multi_4omini.yaml"

    for_n_shapes(data_yml, 3)

