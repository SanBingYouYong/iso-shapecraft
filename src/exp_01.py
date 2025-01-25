'''
Zero-shot One-run Experiment: text description -> pycode -> render+export (image)
'''
from agents import exp_full_task
from combine_and_run import combine_and_run

import os
import yaml
from time import sleep

SHAPE_DESCRIPTIONS_YAML = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\src\\shapes.yaml"

def read_shapes(shapes_yaml: str) -> dict:
    with open(shapes_yaml, 'r') as stream:
        shapes = yaml.safe_load(stream)['shapes']
    return shapes


def one_shape(shape_description: str):
    # Generate the python code
    out = exp_full_task(shape_description)
    exp_id = out['exp_id']
    print(exp_id)
    task_type = out['task_type']
    # result = out['result']  # well this is py code str already but let's re-use file-based combine-and-run method

    output_py = task_type.value["name"] + ".py"

    # Render and export the image
    combine_and_run(exp_id, output_py)

def all_shapes():
    shapes = read_shapes(SHAPE_DESCRIPTIONS_YAML)[:3]
    for shape_description in shapes:
        one_shape(shape_description)
        sleep(1)


if __name__ == "__main__":
    # shape_description = "A red sphere"
    # one_shape(shape_description)
    all_shapes()
