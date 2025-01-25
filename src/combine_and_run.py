'''
Combine a output python file with predefined suffix code, set up json config for blender job and call blender.
'''
import os
import json
import subprocess
import time
from file_utils import get_exp


BLENDER_EXE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe"
BLEND_FILE = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\auto_render.blend"

PROJECT_ROOT = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft"

def paths(exp_folder: str, output_py: str, suffix_py: str, config_json: str, render_folder: str, obj_folder: str):
    exp_folder = os.path.join(PROJECT_ROOT, get_exp(), exp_folder)
    os.makedirs(exp_folder, exist_ok=True)
    output_py = os.path.join(exp_folder, output_py)
    if not os.path.exists(output_py):
        raise FileNotFoundError(f"output_py {output_py} not found")
    suffix_py = os.path.join(PROJECT_ROOT, suffix_py)
    if not os.path.exists(suffix_py):
        raise FileNotFoundError(f"suffix_py {suffix_py} not found")
    config_json = os.path.join(PROJECT_ROOT, config_json)
    if not os.path.exists(config_json):
        raise FileNotFoundError(f"config_json {config_json} not found")
    render_folder = os.path.join(exp_folder, render_folder)
    os.makedirs(render_folder, exist_ok=True)
    obj_folder = os.path.join(exp_folder, obj_folder)
    os.makedirs(obj_folder, exist_ok=True)
    return exp_folder, output_py, suffix_py, config_json, render_folder, obj_folder

def combine_and_run(exp_id: str, output_py: str, 
         suffix_py: str="code_suffix.py", config_json: str="config.json", 
         blender_exe: str=BLENDER_EXE, blend_file: str=BLEND_FILE, 
         render_folder: str="render", obj_folder: str="obj"):
    '''
    output_py: assumed to be under exp_folder/
    exp_folder, suffix_py, combined_py, config_json, render_folder, obj_folder: base names, automatically path-joined
    '''
    # absolute paths and check
    exp_id, output_py, suffix_py, config_json, render_folder, obj_folder = paths(exp_id, output_py, suffix_py, config_json, render_folder, obj_folder)
    combined_py = os.path.join(exp_id, f"_combined_{os.path.basename(output_py).split('.')[0]}.py")
    # check for blend paths
    if not os.path.exists(blender_exe):
        raise FileNotFoundError(f"blender_exe {blender_exe} not found")
    if not os.path.exists(blend_file):
        raise FileNotFoundError(f"blend_file {blend_file} not found")

    # Read and combine files
    with open(output_py, 'r', encoding='utf-8') as f1, open(suffix_py, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
    combined_content = content1 + "\n" + content2
    with open(combined_py, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    # Set config.json
    config = {
        "output_path": exp_id,
        "obj_name": os.path.basename(output_py).split('.')[0]  # use output_py base name as obj_name for now
    }
    with open(config_json, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    # Call Blender
    command = [blender_exe, "-b", blend_file, "-P", combined_py]
    result = subprocess.run(command, capture_output=True, text=True)
    # Log stdout and stderr to separate files
    stdout_log = os.path.join(exp_id, "blender_stdout.log")
    stderr_log = os.path.join(exp_id, "blender_stderr.log")
    
    with open(stdout_log, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    
    with open(stderr_log, 'w', encoding='utf-8') as f:
        f.write(result.stderr)

if __name__ == "__main__":
    combine_and_run(
        exp_id="exp_a",
        output_py="sample_output.py"
    )
