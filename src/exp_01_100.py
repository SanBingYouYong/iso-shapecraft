'''
Zero-shot One-run Experiment: text description -> pycode -> render+export (image)
'''
from agents import exp_full_task_batch_out

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

OUT_FOLDER = os.path.join(
    "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\exp", os.path.basename(SHAPE_DESCRIPTIONS_YAML).split(".")[0]
)

def get_all_pycode(shapes: list, out_folder: str=OUT_FOLDER):
    
    for i in tqdm(range(len(shapes))):
        py_path = os.path.join(out_folder, f"{str(i).zfill(4)}.py")
        json_path = os.path.join(out_folder, f"{str(i).zfill(4)}.json")
        out = exp_full_task_batch_out(shapes[i])
        with open(py_path, "w") as f:
            f.write(out["parsed"])
        with open(json_path, "w") as f:
            json.dump({"messages": [{"role": "user", "content": out["prompt"]}, {"role": "assistant", "content": out["response"]}]}, f)

if __name__ == "__main__":
    shapes = read_shapes(SHAPE_DESCRIPTIONS_YAML)
    os.makedirs(OUT_FOLDER, exist_ok=True)
    get_all_pycode(shapes)
