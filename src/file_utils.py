import os
import yaml
import json

from constants import TaskType

# CONFIG_FILE = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\config.json"
# with open(CONFIG_FILE, 'r') as f:
#     config = json.load(f)
# if "dynamic_exp_folder" in config:
#     dynamic_exp_folder = config["dynamic_exp_folder"]
# else:
#     dynamic_exp_folder = "exp"
dynamic_exp_folder = "exp"

def set_exp(folder: str) -> None:
    global dynamic_exp_folder
    dynamic_exp_folder = folder

def get_exp() -> str:
    return dynamic_exp_folder

def save_output(task_type: TaskType, response: str, output_folder: str=dynamic_exp_folder) -> None:
    output_path = os.path.join(output_folder, f"{task_type.value}.txt")
    with open(output_path, "a") as file:  # append needed when we track component synthesis tasks
        file.write(response)

def log_output_to_exp(task_type: TaskType, result: dict, exp_id: str) -> None:
    exp_folder = os.path.join(dynamic_exp_folder, exp_id)
    os.makedirs(exp_folder, exist_ok=True)
    # save prompt + response as json in openai chat history format, parsed results as corresponding format
    prompt = result["prompt"]
    response = result["response"]
    parsed = result["parsed"]
    with open(os.path.join(exp_folder, f"{task_type.value['name']}_chat.json"), "a") as file:
        json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}, file)
    task_out_format = task_type.value["out"]
    task_name = task_type.value["name"]
    if task_out_format == "yaml":
        with open(os.path.join(exp_folder, f"{task_name}.yaml"), "a") as file:
            yaml.dump(parsed, file)
    elif task_out_format == "txt":
        with open(os.path.join(exp_folder, f"{task_name}.txt"), "a") as file:
            file.write(parsed)
    elif task_out_format == "py":
        with open(os.path.join(exp_folder, f"{task_name}.py"), "a") as file:
            file.write(parsed)
    else:
        raise NotImplementedError(f"Output format {task_out_format} not supported yet.")

def read_as_yaml(file_path: str) -> dict:
    '''
    Reads a plain text file as a yaml file.

    Error handling: let it crash.
    '''
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_as_yaml(text: str) -> dict:
    '''
    Parses a string as a yaml file.

    Error handling: let it crash.
    '''
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as e:
        with open("yaml_parse_backup.txt", "w") as backup_file:
            backup_file.write(text)
        raise ValueError(f"Error parsing yaml: {e}")

