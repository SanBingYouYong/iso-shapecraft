'''
Zero-shot One-run Experiment: text description -> pycode -> render+export (image)
'''
from agents import exp_full_task_batch_out
from combine_and_run import combine_and_run_batched

import os
import yaml
from tqdm import tqdm
import json

# SHAPE_DESCRIPTIONS_YAML = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\src\\shapes.yaml"
SHAPE_DESCRIPTIONS_YAML = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapes_simple_4omini.yaml"

def read_shapes(shapes_yaml: str) -> dict:
    with open(shapes_yaml, 'r') as stream:
        shapes = yaml.safe_load(stream)['shapes']
    return shapes

# for recording llm response and parsed python codes
OUT_FOLDER = os.path.join(
    "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\exp", os.path.basename(SHAPE_DESCRIPTIONS_YAML).split(".")[0]
)
# for recording the results from running the python codes (render + export)
RUN_OUT_FOLDER = OUT_FOLDER + "_blended"


def get_all_pycode(shapes: list, out_folder: str=OUT_FOLDER):
    
    for i in tqdm(range(len(shapes))):
        py_path = os.path.join(out_folder, f"{str(i).zfill(4)}.py")
        json_path = os.path.join(out_folder, f"{str(i).zfill(4)}.json")
        out = exp_full_task_batch_out(shapes[i])
        with open(py_path, "w") as f:
            f.write(out["parsed"])
        with open(json_path, "w") as f:
            json.dump({"messages": [{"role": "user", "content": out["prompt"]}, {"role": "assistant", "content": out["response"]}]}, f)

def run_code_and_render(all_codes_path: str=OUT_FOLDER, out_folder: str=RUN_OUT_FOLDER):
    py_files = [f for f in os.listdir(all_codes_path) if f.endswith('.py')]
    for i in tqdm(range(len(py_files))):
        py_file = py_files[i]
        abs_py = os.path.join(all_codes_path, py_file)
        combine_and_run_batched(abs_py, out_folder)

if __name__ == "__main__":
    # get all code
    # shapes = read_shapes(SHAPE_DESCRIPTIONS_YAML)
    # os.makedirs(OUT_FOLDER, exist_ok=True)
    # get_all_pycode(shapes)

    # run all code
    run_code_and_render()
