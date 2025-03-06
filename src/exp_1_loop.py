from agents import visual_feedback, exp_full_task, exp_single_get_prompt, _extract_python_code, visual_feedback_get_prompts, _extract_yml_code, shape_evaluation, procedural_synth, procedural_synth_get_prompt, one_issue
from chat import llm_with_history, vlm_multi_img
from combine_and_run import combine_and_run_looped
from file_utils import parse_as_yaml

import time
import os
import json
import yaml
import random
from tqdm import tqdm

with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)
PATHS = config["paths"]
PATH_MAX_ITER = config["path_max_iter"]

'''
Initial code -> 
- error detected (in error log or syntax error): add to original dialogue with "Error encountered: ..."
- no error: show multi-view rendered images to VLM feedback agent, add feedback to original dialogue
'''

def format_feedback(feedback: str) -> str:
    return f"Please update the code based on the feedback: \n{feedback}"


def one_shape_single_loop(shape_description: str, exp_folder_abs: str):
    '''
    Expects a shape description and an experiment folder (absolute path!) to output to.
    '''
    os.makedirs(exp_folder_abs, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder_abs) != []:
        # delete everything
        for f in os.listdir(exp_folder_abs):
            os.remove(os.path.join(exp_folder_abs, f))
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
        pycode_path = os.path.join(exp_folder_abs, f"{str(ite)}.py")  # use ite as basename
        with open(pycode_path, "w") as f:
            f.write(pycode)
        combine_and_run_looped(pycode_path, exp_folder_abs)
        # check for successful execution by: stderr log's "An error occurred:" line, or {ite}_syntax_error.txt, or images exists
        syntax_error = os.path.join(exp_folder_abs, f"{str(ite)}_syntax_error.txt")
        if os.path.exists(syntax_error):
            with open(syntax_error, "r") as f:
                error = f.read()
            prompt = f"Error encountered: {error}"
            ite += 1
            continue
        # if no syntax error, check stderr log
        error_log = os.path.join(exp_folder_abs, f"{str(ite)}_blender_stderr.log")
        with open(error_log, "r") as f:
            error = f.read()
        if "An error occurred:" in error:
            error_lines = error.split("\n")  # skips the universal TBmalloc warning and the flag line itself
            error = error_lines[error_lines.index("An error occurred:"):]
            error_str = "\n".join(error)
            prompt = f"Error encountered: {error_str}"
            ite += 1
            continue
        # if no errors from above two checks, images should definitely be in place
        # find current iteration prefxied images
        images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(ite)}_") and f.endswith('.png')]
        image_paths = [os.path.join(exp_folder_abs, img) for img in images]
        if len(images) == 0:
            raise ValueError(f"No images found for iteration {ite}.")
        for img in images:
            assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
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
        try:
            feedback_yml = _extract_yml_code(feedback)
            parsed_feedback = parse_as_yaml(feedback_yml)
            assert "issues" in parsed_feedback and "consistency" in parsed_feedback, f"Feedback parsing failed: {parsed_feedback}"
        except:
            print(f"Feedback parsing failed: {feedback}")
            parsed_feedback = feedback
        if parsed_feedback['consistency']:  # yaml handles parsing multiple ways of saying True already
            done = True
            # print(f"Task completed in {ite} iterations.")
        else:
            prompt = format_feedback(feedback)
            ite += 1
    # save final history
    with open(os.path.join(exp_folder_abs, "history.json"), "w") as f:
        json.dump(history, f)
    # save visual feedbacks
    with open(os.path.join(exp_folder_abs, "feedback.json"), "w") as f:
        json.dump(visual_feedbacks, f)
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, "shape_description.txt"), "w") as f:
        f.write(shape_description)
    return ite, history

def one_shape_multi_path(shape_description: str, exp_folder_abs: str):
    '''
    Expects a shape description and an experiment folder (absolute path!) to output to.
    
    foreach path foreach iteration, if execution successful then run evaluation and store results
    '''
    os.makedirs(exp_folder_abs, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder_abs) != []:
        # delete everything
        for f in os.listdir(exp_folder_abs):
            os.remove(os.path.join(exp_folder_abs, f))
    paths = 3
    path_max_iter = 3
    evaluation_prompt_record = None
    evaluation_history = []
    evaluations = []
    for path in range(paths):
        if done:
            break
        print(f"Processing path {path}...")
        ite = 0
        history = []
        done = False
        visual_feedbacks = []
        prompt = exp_single_get_prompt(shape_description)
        while not done and ite < path_max_iter:
            print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            pycode = _extract_python_code(response)
            if pycode == "":
                raise ValueError("No python code extracted from LLM response.")
            pycode_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.py")
            with open(pycode_path, "w") as f:
                f.write(pycode)
            combine_and_run_looped(pycode_path, exp_folder_abs)
            # check for successful execution
            syntax_error = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_syntax_error.txt")
            if os.path.exists(syntax_error):
                with open(syntax_error, "r") as f:
                    error = f.read()
                prompt = f"Error encountered: {error}"
                ite += 1
                continue
            # if no syntax error, check stderr log
            error_log = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_blender_stderr.log")
            with open(error_log, "r") as f:
                error = f.read()
            if "An error occurred:" in error:
                error_lines = error.split("\n")
                error = error_lines[error_lines.index("An error occurred:"):]
                error_str = "\n".join(error)
                prompt = f"Error encountered: {error_str}"
                ite += 1
                continue
            # if no errors from above two checks, images should definitely be in place
            images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(path)}_{str(ite)}_") and f.endswith('.png')]
            image_paths = [os.path.join(exp_folder_abs, img) for img in images]
            if len(images) == 0:
                raise ValueError(f"No images found for iteration {ite}.")
            for img in images:
                assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
            # evaluation
            eval_result = shape_evaluation(shape_description, image_paths)
            print(f"Evaluation result: {eval_result['parsed']}")
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
                (score, pycode_path)
            )
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
            try:
                feedback_yml = _extract_yml_code(feedback)
                parsed_feedback = parse_as_yaml(feedback_yml)
                assert "issues" in parsed_feedback and "consistency" in parsed_feedback, f"Feedback parsing failed: {parsed_feedback}"
                if parsed_feedback['consistency']:  # yaml handles parsing multiple ways of saying True already
                    done = True
            except:
                print(f"Feedback parsing failed: {feedback}")
                parsed_feedback = feedback
            prompt = format_feedback(feedback)
            ite += 1
        # save final history
        with open(os.path.join(exp_folder_abs, f"{str(path)}_history.json"), "w") as f:
            json.dump(history, f)
        # save evaluation history
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_history.json"), "w") as f:
            json.dump(evaluation_history, f)
        # save evaluations
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluations.json"), "w") as f:
            json.dump(evaluations, f)
        # save evaluation prompt used
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_prompt.md"), "w") as f:
            f.write(evaluation_prompt_record)
        # save visual feedbacks
        with open(os.path.join(exp_folder_abs, f"{str(path)}_feedback.json"), "w") as f:
            json.dump(visual_feedbacks, f)
        # add a short indicator to record the shape description
        with open(os.path.join(exp_folder_abs, f"{str(path)}_shape_description.txt"), "w") as f:
            f.write(shape_description)
    # choose best
    best_score, best_py_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_py_path": best_py_path,
    }

def one_shape_multi_path_evaluation_as_feedback(shape_description: str, exp_folder_abs: str):
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
    paths = 3
    path_max_iter = 3
    evaluation_prompt_record = None
    evaluation_history = []
    done = False
    evaluations = []
    for path in range(paths):
        if done:
            break
        # print(f"Processing path {path}...")
        ite = 0
        history = []
        prompt = exp_single_get_prompt(shape_description)
        while not done and ite < path_max_iter:
            # print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            pycode = _extract_python_code(response)
            if pycode == "":
                raise ValueError("No python code extracted from LLM response.")
            pycode_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.py")
            with open(pycode_path, "w") as f:
                f.write(pycode)
            combine_and_run_looped(pycode_path, exp_folder_abs)
            # check for successful execution
            syntax_error = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_syntax_error.txt")
            if os.path.exists(syntax_error):
                with open(syntax_error, "r") as f:
                    error = f.read()
                prompt = f"Error encountered: {error}"
                ite += 1
                continue
            # if no syntax error, check stderr log
            error_log = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_blender_stderr.log")
            with open(error_log, "r") as f:
                error = f.read()
            if "An error occurred:" in error:
                error_lines = error.split("\n")
                error = error_lines[error_lines.index("An error occurred:"):]
                error_str = "\n".join(error)
                prompt = f"Error encountered: {error_str}"
                ite += 1
                continue
            # if no errors from above two checks, images should definitely be in place
            images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(path)}_{str(ite)}_") and f.endswith('.png')]
            image_paths = [os.path.join(exp_folder_abs, img) for img in images]
            if len(images) == 0:
                raise ValueError(f"No images found for iteration {ite}.")
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
                (score, pycode_path)
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
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_history.json"), "w") as f:
            json.dump(evaluation_history, f)
        # save evaluations
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluations.json"), "w") as f:
            json.dump(evaluations, f)
        # save evaluation prompt used
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_prompt.md"), "w") as f:
            f.write(evaluation_prompt_record)
        # add a short indicator to record the shape description
        with open(os.path.join(exp_folder_abs, f"{str(path)}_shape_description.txt"), "w") as f:
            f.write(shape_description)
    # choose best
    best_score, best_py_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_py_path": best_py_path,
    }

def one_shape_mp_eaf_procedural(shape_name: str, shape_description: str, exp_folder_abs: str):
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
    paths = 3
    path_max_iter = 3
    evaluation_prompt_record = None
    evaluation_history = []
    done = False
    evaluations = []
    for path in range(paths):
        if done:
            break
        # print(f"Processing path {path}...")
        ite = 0
        history = []
        prompt = procedural_synth_get_prompt(shape_name, shape_description)
        while not done and ite < path_max_iter:
            # print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            pycode = _extract_python_code(response)
            if pycode == "":
                raise ValueError("No python code extracted from LLM response.")
            pycode_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.py")
            with open(pycode_path, "w") as f:
                f.write(pycode)
            combine_and_run_looped(pycode_path, exp_folder_abs)
            # check for successful execution
            syntax_error = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_syntax_error.txt")
            if os.path.exists(syntax_error):
                with open(syntax_error, "r") as f:
                    error = f.read()
                prompt = f"Error encountered: {error}"
                ite += 1
                continue
            # if no syntax error, check stderr log
            error_log = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_blender_stderr.log")
            with open(error_log, "r") as f:
                error = f.read()
            if "An error occurred:" in error:
                error_lines = error.split("\n")
                error = error_lines[error_lines.index("An error occurred:"):]
                error_str = "\n".join(error)
                prompt = f"Error encountered: {error_str}"
                ite += 1
                continue
            # if no errors from above two checks, images should definitely be in place
            images = [f for f in os.listdir(exp_folder_abs) if f.startswith(f"{str(path)}_{str(ite)}_") and f.endswith('.png')]
            image_paths = [os.path.join(exp_folder_abs, img) for img in images]
            if len(images) == 0:
                raise ValueError(f"No images found for iteration {ite}.")
            for img in images:
                assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
            # evaluation
            eval_str = f"name: {shape_name}\ndescription: {shape_description}"
            eval_result = shape_evaluation(eval_str, image_paths)
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
                (score, pycode_path)
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
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_history.json"), "w") as f:
            json.dump(evaluation_history, f)
        # save evaluations
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluations.json"), "w") as f:
            json.dump(evaluations, f)
        # save evaluation prompt used
        with open(os.path.join(exp_folder_abs, f"{str(path)}_evaluation_prompt.md"), "w") as f:
            f.write(evaluation_prompt_record)
        # add a short indicator to record the shape description
        with open(os.path.join(exp_folder_abs, f"{str(path)}_shape.txt"), "w") as f:
            f.write(shape_name)
            f.write("\n")
            f.write(shape_description)
    # choose best
    best_score, best_py_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_py_path": best_py_path,
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
    evaluation_prompt_record = ""
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
        prompt = exp_single_get_prompt(shape_description)
        while not done and ite < path_max_iter:
            # print(f" - Iteration {ite}...")
            response, history = llm_with_history(prompt, history)
            py_code = _extract_python_code(response)
            if py_code == "":
                raise ValueError(f"No Python code extracted from LLM response. {response}")
            py_code_path = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}.py")
            with open(py_code_path, "w") as f:
                f.write(py_code)
            # run_openscad(scad_code_path, exp_folder_abs)
            # run_render_export(scad_code_path, exp_folder_abs)
            combine_and_run_looped(py_code_path, exp_folder_abs)
            # check for successful execution
            syntax_error = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_syntax_error.txt")
            if os.path.exists(syntax_error):
                with open(syntax_error, "r") as f:
                    error = f.read()
                prompt = f"Error encountered: {error}"
                ite += 1
                continue
            # if no syntax error, check stderr log
            error_log = os.path.join(exp_folder_abs, f"{str(path)}_{str(ite)}_blender_stderr.log")
            with open(error_log, "r") as f:
                error = f.read()
            if "An error occurred:" in error:
                error_lines = error.split("\n")
                error = error_lines[error_lines.index("An error occurred:"):]
                error_str = "\n".join(error)
                prompt = f"Error encountered: {error_str}"
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
            one_issue_feedback = one_issue(shape_description, image_paths)['response']
            prompt = format_feedback(one_issue_feedback)
            # evaluation
            eval_result = shape_evaluation(shape_description, image_paths)
            # print(f"Evaluation result: {eval_result['parsed']}")
            if evaluation_prompt_record == "":
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
                (score, py_code_path)
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
    if len(evaluations) == 0:  # in case none is successful
        return {
            "best_score": 0,
            "best_code_path": "",
        }
    best_score, best_code_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_code_path": best_code_path,
    }

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
        ite, hist = one_shape_single_loop(shape, shape_out_root)
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
        ite, hist = one_shape_single_loop(shape, os.path.join(exp_out_root, f"{str(i).zfill(4)}"))
        iterations.append(ite)
    with open(os.path.join(exp_out_root, "iterations.csv"), "w") as f:
        f.write("\n".join([str(i) for i in iterations]))

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
    exp_root = f"eval_python_single_{n}x_{os.path.basename(data_yml).split('.')[0]}"
    for i in tqdm(range(len(data)), desc="Processing shapes"):
        shape_description = data[i]
        exp_folder_abs = os.path.abspath(os.path.join("exp", exp_root, f"shape_{i:04d}"))
        result = one_shape_mp_one_issue(shape_description, exp_folder_abs)
    print("Operation completed successfully.")

def cadprompt_test(data_yml: str, n: int=1, sample=False):
    '''
    data_yml: str (absolute path)
    n: int
    '''
    with open(data_yml, "r") as f:
        data = yaml.safe_load(f)
    if sample:
        data = random.sample(data, min(n, len(data)))
    else:
        if len(data) < n:
            n = len(data)
        keys = list(data.keys())
        data = [data[k] for k in keys[:n]]
    exp_root = f"cadprompt_test_{n}x_{os.path.basename(data_yml).split('.')[0]}"
    for i in tqdm(range(len(data)), desc="Processing shapes"):
        shape_description = data[i]['parsed_shape_description']
        exp_folder_abs = os.path.abspath(os.path.join("exp", exp_root, f"shape_{i:04d}"))
        result = one_shape_mp_one_issue(shape_description, exp_folder_abs)
    print("Operation completed successfully.")
# NOTE: make sure to update config.yaml accordingly with programming language
if __name__ == "__main__":
    # shape = "A chair with four legs, a backrest, no armrests, and a cushioned seat."
    # timestamp = time.strftime("%m%d-%H%M%S")
    # exp_out_root = f"exp\\looped\\{timestamp}"
    # one_shape_looped(shape, os.path.abspath(exp_out_root))

    # loop_10_daily_objects()

    # all_shapes_looped(67, os.path.abspath("exp\\single_daily_shapes_looped_all_0202-181517"))  # manual skip index for resuming
    # all_shapes_looped(39, os.path.abspath("exp\\single_daily_shapes_looped_all_0202-221821"))  # manual skip index for resuming

    # bests = one_shape_multi_path("A chair", os.path.abspath("exp\\multi_path_test\\chair"))
    # print(bests)
    # combine_and_run_looped(bests['best_py_path'], os.path.abspath("exp\\multi_path_test\\chair_best"))
    
    # bests = one_shape_multi_path_evaluation_as_feedback("A chair", os.path.abspath("exp\\multi_path_test_eaf\\chair"))
    # print(bests)
    # combine_and_run_looped(bests['best_py_path'], os.path.abspath("exp\\multi_path_test_eaf\\chair_best"))

    # bests = one_shape_mp_eaf_procedural("A chair", "A chair with four legs, a backrest, no armrests, and a cushioned seat.", os.path.abspath("exp\\mp_eaf_procedural\\chair"))
    # print(bests)
    # combine_and_run_looped(bests['best_py_path'], os.path.abspath("exp\\mp_eaf_procedural\\chair_best"))

    # shape_description = "A cylindrical coffee mug with a handle on the side."
    # exp_folder_abs = os.path.abspath(os.path.join("exp", "manual", "python_coffee_mug_single"))
    # # result = one_shape_mp_eaf(shape_description, exp_folder_abs)
    # result = one_shape_mp_one_issue(shape_description, exp_folder_abs)
    # print(result)
    # print("Operation completed successfully.")
    
    # data_yml = "dataset/shapes_daily_multistruct_4omini.yaml"
    # data_yml = "dataset/shapes_simple_4omini.yaml"
    # data_yml = "dataset/shapes_daily_4omini.yaml"
    # data_yml = "dataset/shapes_primitive_multi_4omini.yaml"

    data_yml = "dataset/cadprompt_parsed.yml"

    # for_n_shapes(data_yml, 10)
    cadprompt_test(data_yml, 10)

