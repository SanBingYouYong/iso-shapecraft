import os
import yaml

from constants import TaskType

def _save_output(task_type: TaskType, response: str, output_folder: str) -> None:
    output_path = os.path.join(output_folder, f"{task_type.value}.txt")
    with open(output_path, "a") as file:  # append needed when we track component synthesis tasks
        file.write(response)

def _read_as_yaml(file_path: str) -> dict:
    '''
    Reads a plain text file as a yaml file.

    Error handling: let it crash.
    '''
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def _parse_as_yaml(text: str) -> dict:
    '''
    Parses a string as a yaml file.

    Error handling: let it crash.
    '''
    return yaml.safe_load(text)

