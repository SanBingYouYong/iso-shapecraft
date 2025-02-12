from exp_1_loop import one_shape_single_loop, one_shape_multi_path_evaluation_as_feedback, one_shape_mp_eaf_procedural, one_shape_mp_one_issue
from agents import task_decomp_get_prompt, parse_as_yaml, _extract_python_code, _extract_yml_code, high_level_aggregation_get_prompt, code_level_aggregation_get_prompt, visual_feedback_get_prompts, shape_evaluation, one_issue
from chat import llm_with_history, vlm_multi_img
from combine_and_run import combine_and_run_looped

import yaml
import os
import json
from tqdm import tqdm
import random

with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)
PATHS = config["paths"]
PATH_MAX_ITER = config["path_max_iter"]

def format_feedback(feedback: str) -> str:
    return f"Please update the code based on the feedback: \n{feedback}"

def full_aggregation_single_loop(aggregator_prompt, sub_task_codes, shape_description, exp_folder_abs):
    '''
    aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
    '''
    os.makedirs(exp_folder_abs, exist_ok=True)
    # Check if the folder contains any content
    if os.listdir(exp_folder_abs) != []:
        # delete everything
        for f in os.listdir(exp_folder_abs):
            os.remove(os.path.join(exp_folder_abs, f))
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, "shape_description.txt"), "w") as f:
        f.write(shape_description)
    done = False
    max_ite = 5
    ite = 0
    history = []
    prompt = code_level_aggregation_get_prompt(aggregator_prompt, sub_task_codes)
    visual_feedbacks = []
    while not done and ite < max_ite:
        # print(f"Iteration {ite}...")
        response, history = llm_with_history(prompt, history)
        pycode = _extract_python_code(response)
        if pycode == "":
            raise ValueError(f"No python code extracted from LLM response at iteration {ite}, response: {response}.")
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
    with open(os.path.join(exp_folder_abs, "history.json"), "w") as f:
        json.dump(history, f)
    # save visual feedbacks
    with open(os.path.join(exp_folder_abs, "feedback.json"), "w") as f:
        json.dump(visual_feedbacks, f)
    
    return ite, history

# EVAL: tested 10 daily
def full_aggregation_multi_path_eaf(aggregator_prompt, sub_task_codes, shape_description, exp_folder_abs, paths=PATHS, path_max_iter=PATH_MAX_ITER):
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
        prompt = code_level_aggregation_get_prompt(aggregator_prompt, sub_task_codes)
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
                raise ValueError(f"No images found for iteration {ite}, path {path} at {exp_folder_abs}.")
            for img in images:
                assert os.path.exists(os.path.join(exp_folder_abs, img)), f"Image {img} not found."
            # one issue feedback
            one_issue_feedback = one_issue(shape_description, image_paths)['response']
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
                (score, pycode_path)
            )
            # feedback = eval_result['parsed']['explanation']
            # prompt = format_feedback(feedback)
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
    if len(evaluations) == 0:
        return {
            "best_score": 0,
            "best_py_path": "",
        }
    best_score, best_py_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_code_path": best_py_path,
    }

# TODO: exactly the same as non-procedural, but see if we want to design a new prompt
def full_aggregation_mp_eaf_procedural(aggregator_prompt, sub_task_codes, shape_description, exp_folder_abs):
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
        prompt = code_level_aggregation_get_prompt(aggregator_prompt, sub_task_codes)
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
            if evaluation_prompt_record is not None:
                f.write(evaluation_prompt_record)
        
    # choose best
    best_score, best_py_path = max(evaluations, key=lambda x: x[0])
    return {
        "best_score": best_score,
        "best_py_path": best_py_path,
    }


def test_full_shape_looped():
    code_1_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0000"))
    with open(code_1_path, "r") as f:
        code_1 = f.read()
    code_2_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0001"))
    with open(code_2_path, "r") as f:
        code_2 = f.read()
    full_aggregation_single_loop(
        "Place the mug on top of the plate while keeping the mug centered on the plate.",
        {
            "mug": code_1,
            "plate": code_2
        },
        "A mug on a plate",
        os.path.abspath("exp/full_shape_looped_test")
    )

def test_full_shape_multi_path_eaf():
    code_1_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0000"))
    with open(code_1_path, "r") as f:
        code_1 = f.read()
    code_2_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0001"))
    with open(code_2_path, "r") as f:
        code_2 = f.read()
    full_aggregation_multi_path_eaf(
        "Place the mug on top of the plate while keeping the mug centered on the plate.",
        {
            "mug": code_1,
            "plate": code_2
        },
        "A mug on a plate",
        os.path.abspath("exp/full_shape_looped_eaf_test")
    )

def get_latest_working_pycode(sub_task_folder):
    '''
    Latest: based on file suffix index (only 0.py not 0_combined.py)
    Working: its iteration contains renderings and obj files (not check error logs for now)

    Returns the path to the latest working pycode file, or None if not found.
    '''
    pycode_files = [f for f in os.listdir(sub_task_folder) if f.endswith('.py')]
    pycode_files = [f for f in pycode_files if not f.endswith('_combined.py')]
    pycode_files.sort(key=lambda x: int(x.split('.')[0]))
    pycode_files.reverse()  # latest first
    for pycode_file in pycode_files:
        ite = pycode_file.split('.')[0]
        if os.path.exists(os.path.join(sub_task_folder, f"{ite}_0.png")) and os.path.exists(os.path.join(sub_task_folder, f"{ite}.obj")):
            return os.path.join(sub_task_folder, pycode_file)
    return None
    
def components_one_looped(sub_tasks, exp_root_folder_abs):
    sub_task_codes = {}
    # for each sub-task:
    for i, sub_task in enumerate(sub_tasks):
        sub_task_name = sub_task['name']
        sub_task_desc = sub_task['description']
        sub_task_folder = os.path.join(exp_root_folder_abs, f"sub_task_{i}_{sub_task_name}")
        # sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
        one_shape_single_loop(sub_task_desc, sub_task_folder)
        # find latest pycode file
        latest_working_pycode_file = get_latest_working_pycode(sub_task_folder)
        if latest_working_pycode_file is None:
            raise ValueError(f"No working pycode file found for sub-task {sub_task_name}.")
        with open(latest_working_pycode_file, "r") as f:
            sub_task_codes[sub_task_name] = f.read()
    return sub_task_codes

# EVAL: tested 10 daily
def components_multi_pathed(sub_tasks, exp_root_folder_abs):
    sub_task_codes = {}
    # for each sub-task:
    for i, sub_task in enumerate(sub_tasks):
        sub_task_name = sub_task['name']
        sub_task_desc = sub_task['description']
        description_str = f"shape to be modeled: {sub_task_name}\nshape description: {sub_task_desc}"
        sub_task_folder = os.path.join(exp_root_folder_abs, f"sub_task_{i}_{sub_task_name}")
        # sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
        # bests = one_shape_multi_path_evaluation_as_feedback(description_str, sub_task_folder)
        bests = one_shape_mp_one_issue(description_str, sub_task_folder)
        best_py_path = bests['best_code_path']
        with open(best_py_path, "r") as f:
            sub_task_codes[sub_task_name] = f.read()
    return sub_task_codes

def components_mp_procedural(sub_tasks, exp_root_folder_abs):
    sub_task_codes = {}
    # for each sub-task:
    for i, sub_task in enumerate(sub_tasks):
        sub_task_name = sub_task['name']
        sub_task_desc = sub_task['description']
        sub_task_folder = os.path.join(exp_root_folder_abs, f"sub_task_{i}")
        # sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
        bests = one_shape_mp_eaf_procedural(sub_task_name, sub_task_desc, sub_task_folder)
        best_py_path = bests['best_py_path']
        with open(best_py_path, "r") as f:
            sub_task_codes[sub_task_name] = f.read()
    return sub_task_codes
        
# EVAL: tested 10 daily
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
    
    # sub_task_codes = components_one_looped(sub_tasks, exp_root_folder_abs)
    sub_task_codes = components_multi_pathed(sub_tasks, exp_root_folder_abs)
    # sub_task_codes = components_mp_procedural(sub_tasks, exp_root_folder_abs)
    
    # (high-level) shape description + sub-tasks (text) -llm> aggregator prompt (text) [root/aggregator_folder]
    high_aggregator_prompt = high_level_aggregation_get_prompt(shape_description, sub_tasks)
    code_aggregator_prompt, high_aggre_history = llm_with_history(high_aggregator_prompt, [])
    with open(os.path.join(exp_root_folder_abs, "high_aggregator.json"), "w") as f:
        json.dump(high_aggre_history, f)
    
    # (code-level) aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
    aggre_folder = os.path.join(exp_root_folder_abs, "aggregator")
    try:
        # full_aggregation_single_loop(code_aggregator_prompt, sub_task_codes, shape_description, aggre_folder)
        full_aggregation_multi_path_eaf(code_aggregator_prompt, sub_task_codes, shape_description, aggre_folder)
    except Exception as e:
        print(f"Error in full_shape_looped: {e}")
    return aggre_folder


def for_n_shapes(data_yml: str, n: int=3, sample=False, skip_n=0):
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
    exp_root = f"eval_python_full_{n}x_{os.path.basename(data_yml).split('.')[0]}"
    for i in tqdm(range(len(data)), desc="Processing shapes"):
        if i < skip_n:
            continue
        shape_description = data[i]
        exp_folder_abs = os.path.abspath(os.path.join("exp", exp_root, f"shape_{i:04d}"))
        result = full_pipeline(shape_description, exp_folder_abs)
    print("Operation completed successfully.")


if __name__ == "__main__":
    # test full_shape_looped with pre-defined inputs
    # test_full_shape_looped()
    # test full_shape_multi_path_eaf with pre-defined inputs
    # test_full_shape_multi_path_eaf()
    # full test
    # full_pipeline("A cylindrical water bottle with a screw-on cap and a transparent body.", os.path.abspath("exp/manual/python_bottle_procedural"))
    random.seed(0)

    # data_yml = "dataset/shapes_daily_multistruct_4omini.yaml"
    # data_yml = "dataset/shapes_simple_4omini.yaml"
    data_yml = "dataset/shapes_daily_4omini.yaml"
    # data_yml = "dataset/shapes_primitive_multi_4omini.yaml"

    for_n_shapes(data_yml, 10, skip_n=5)  # 断点续传

