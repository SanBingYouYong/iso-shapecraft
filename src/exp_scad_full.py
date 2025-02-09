from openscad_utils import run_openscad, run_render_export
from agents import llm_with_history, exp_single_get_prompt_scad, _extract_openscad_code, shape_evaluation, format_feedback, task_decomp_get_prompt, parse_as_yaml, high_level_aggregation_get_prompt, code_level_aggregation_get_prompt
from exp_scad_single import one_shape_mp_eaf

import os
import json
import yaml
from tqdm import tqdm

def full_aggregation_multi_path_eaf(aggregator_prompt, sub_task_codes, shape_description, exp_folder_abs):
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
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, f"shape_description.txt"), "w") as f:
        f.write(shape_description)
    for path in range(paths):
        if done:
            break
        # print(f"Processing path {path}...")
        ite = 0
        history = []
        prompt = code_level_aggregation_get_prompt(aggregator_prompt, sub_task_codes, lang='openscad')
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
        if evaluation_prompt_record is not None:
            f.write(evaluation_prompt_record)
    # choose best
    best_score, best_code_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_code_path": best_code_path,
    }


def components_multi_pathed(sub_tasks, exp_root_folder_abs):
    sub_task_codes = {}
    # for each sub-task:
    for i, sub_task in enumerate(sub_tasks):
        sub_task_name = sub_task['name']
        sub_task_desc = sub_task['description']
        description_str = f"shape to be modeled: {sub_task_name}\nshape description: {sub_task_desc}"
        sub_task_folder = os.path.join(exp_root_folder_abs, f"sub_task_{i}")
        # sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
        bests = one_shape_mp_eaf(description_str, sub_task_folder)
        best_py_path = bests['best_code_path']
        with open(best_py_path, "r") as f:
            sub_task_codes[sub_task_name] = f.read()
    return sub_task_codes


def full_pipeline(shape_description, exp_root_folder_abs):
    '''
    shape description (text) -llm> sub-tasks (yaml) [exp/exp_root_folder]
    for each sub-task:
        sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
    shape description + sub-tasks (text) -llm> aggregator prompt (text) [root/aggregator_folder]
    aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
    
    shape_description: str
    exp_root_folder: str (absolute path)
    '''
    if not os.path.exists(exp_root_folder_abs):
        os.makedirs(exp_root_folder_abs)
    shape_desc_path = os.path.join(exp_root_folder_abs, "shape_description.txt")
    with open(shape_desc_path, "w") as f:
        f.write(shape_description)
    # shape description (text) -llm> sub-tasks (yaml) [exp/exp_root_folder]
    decomp = task_decomp_get_prompt(shape_description)
    response, history = llm_with_history(decomp, [])
    with open(os.path.join(exp_root_folder_abs, "task_decomposition.json"), "w") as f:
        json.dump(history, f)
    sub_tasks = parse_as_yaml(response)
    sub_tasks_yml = os.path.join(exp_root_folder_abs, "sub_tasks.yml")
    with open(sub_tasks_yml, "w") as f:
        yaml.dump(sub_tasks, f)
    sub_tasks = sub_tasks['components']
    
    sub_task_codes = components_multi_pathed(sub_tasks, exp_root_folder_abs)
    
    # (high-level) shape description + sub-tasks (text) -llm> aggregator prompt (text) [root/aggregator_folder]
    high_aggregator_prompt = high_level_aggregation_get_prompt(shape_description, sub_tasks)
    code_aggregator_prompt, high_aggre_history = llm_with_history(high_aggregator_prompt, [])
    with open(os.path.join(exp_root_folder_abs, "high_aggregator.json"), "w") as f:
        json.dump(high_aggre_history, f)
    
    # (code-level) aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
    aggre_folder = os.path.join(exp_root_folder_abs, "aggregator")
    try:
        full_aggregation_multi_path_eaf(code_aggregator_prompt, sub_task_codes, shape_description, aggre_folder)
    except Exception as e:
        print(f"Error in full_shape_looped: {e}")
    return aggre_folder

def for_n_shapes(data_yml: str, n: int=3):
    '''
    data_yml: str (absolute path)
    n: int
    '''
    with open(data_yml, "r") as f:
        data = yaml.safe_load(f)['shapes']
    if len(data) < n:
        n = len(data)
    exp_root = f"scad_exp_{n}x_{os.path.basename(data_yml).split('.')[0]}"
    for i in tqdm(range(n), desc="Processing shapes"):
        shape_description = data[i]
        exp_folder_abs = os.path.abspath(os.path.join("exp", exp_root, f"shape_{i:04d}"))
        result = full_pipeline(shape_description, exp_folder_abs)
    print("Operation completed successfully.")

if __name__ == "__main__":
    shape_description = "A book lying flat on a table, one chair on each side."
    exp_folder_abs = os.path.abspath(os.path.join("exp", "scene", "book_table_chairs"))
    result = full_pipeline(shape_description, exp_folder_abs)
    print(result)
    print("Operation completed successfully.")


    # data_yml = "dataset/shapes_daily_multistruct_4omini.yaml"
    # data_yml = "dataset/shapes_simple_4omini.yaml"
    # data_yml = "dataset/shapes_daily_4omini.yaml"

    # for_n_shapes(data_yml, 3)
