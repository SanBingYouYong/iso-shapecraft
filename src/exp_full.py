from exp_1_loop import one_shape_looped
from agents import task_decomp_get_prompt, parse_as_yaml, _extract_python_code, _extract_yml_code, high_level_aggregation_get_prompt, code_level_aggregation_get_prompt, visual_feedback_get_prompts
from chat import llm_with_history, vlm_multi_img
from combine_and_run import combine_and_run_looped

import yaml
import os
import json

def format_feedback(feedback: str) -> str:
    return f"Please update the code based on the feedback: \n{feedback}"

def full_shape_looped(aggregator_prompt, sub_task_codes, shape_description, exp_folder_abs):
    '''
    aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
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
    prompt = code_level_aggregation_get_prompt(aggregator_prompt, sub_task_codes)
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
            error = error_lines[error_lines.index("An error occurred:") + 1]
            prompt = f"Error encountered: {error}"
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
    # add a short indicator to record the shape description
    with open(os.path.join(exp_folder_abs, "shape_description.txt"), "w") as f:
        f.write(shape_description)
    return ite, history

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
    
    sub_task_codes = {}
    # for each sub-task:
    for i, sub_task in enumerate(sub_tasks):
        sub_task_name = sub_task['name']
        sub_task_desc = sub_task['description']
        sub_task_folder = os.path.join(exp_root_folder_abs, f"sub_task_{i}_{sub_task_name}")
        # sub-task description (text) -> one_shape_looped (pycode) [root/sub-task_folder]
        one_shape_looped(sub_task_desc, sub_task_folder)
        # find latest pycode file
        latest_working_pycode_file = get_latest_working_pycode(sub_task_folder)
        if latest_working_pycode_file is None:
            raise ValueError(f"No working pycode file found for sub-task {sub_task_name}.")
        with open(latest_working_pycode_file, "r") as f:
            sub_task_codes[sub_task_name] = f.read()
    
    # (high-level) shape description + sub-tasks (text) -llm> aggregator prompt (text) [root/aggregator_folder]
    high_aggregator_prompt = high_level_aggregation_get_prompt(shape_description, sub_tasks)
    code_aggregator_prompt, high_aggre_history = llm_with_history(high_aggregator_prompt, [])
    with open(os.path.join(exp_root_folder_abs, "high_aggregator.json"), "w") as f:
        json.dump(high_aggre_history, f)
    
    # (code-level) aggregator prompt + sub-task code (text) -> full_shape_looped (pycode) [root/aggregator_folder]
    aggre_folder = os.path.join(exp_root_folder_abs, "aggregator")
    full_shape_looped(code_aggregator_prompt, sub_task_codes, shape_description, aggre_folder)

def test_full_shape_looped():
    code_1_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0000"))
    with open(code_1_path, "r") as f:
        code_1 = f.read()
    code_2_path = get_latest_working_pycode(os.path.abspath("exp/single_daily_shapes_looped_all_0202-221821/0001"))
    with open(code_2_path, "r") as f:
        code_2 = f.read()
    full_shape_looped(
        "Place the mug on top of the plate while keeping the mug centered on the plate.",
        {
            "mug": code_1,
            "plate": code_2
        },
        "A mug on a plate",
        os.path.abspath("exp/full_shape_looped_test")
    )

if __name__ == "__main__":
    # test full_shape_looped with pre-defined inputs
    # test_full_shape_looped()
    # full test
    full_pipeline("A coffee mug", os.path.abspath("exp/full/coffe_mug"))

