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

SUFFIX_PY = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\code_suffix.py"
CONFIG_JSON = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\config.json"

STL_PYFILE = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\render_stl.py"
STL_JSON = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\stl_config.json"

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

def combine_and_run_batched(abs_path_py: str, abs_path_out_folder: str, 
                            suffix_py: str=SUFFIX_PY, config_json: str=CONFIG_JSON):
    '''
    abs_path_py: absolute path to the py file to be combined
    abs_path_out_folder: absolute path to the output folder
    '''
    base = os.path.basename(abs_path_py).split('.')[0]
    os.makedirs(abs_path_out_folder, exist_ok=True)
    # Read and combine files
    with open(abs_path_py, 'r', encoding='utf-8') as f1, open(suffix_py, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
    # add a try except block to content1 (src llm shape script)
    import_line = "import sys\nimport traceback\n"
    flag0_line = "success = True\n"
    try_line = "try:\n"
    except_line = "except Exception as e:\n"
    print_line = "    print('An error occurred:', file=sys.stderr)\n"
    traceback_line = "    traceback.print_exc(file=sys.stderr)\n"
    flush_line = "    sys.stderr.flush()  # Ensure that the error output is flushed\n"
    flag1_line = "    success = False\n"
    blender_quit_line = "    bpy.ops.wm.quit_blender()\n"  # somehow either of blender quit or python quit can't solve the problem
    everyline_tab = "    "
    content1 = import_line + flag0_line + try_line + everyline_tab + content1.replace('\n', '\n' + everyline_tab) + '\n' + except_line + print_line + traceback_line + flush_line + flag1_line + blender_quit_line
    combined_content = content1 + "\n" + content2
    abs_path_combined_py = os.path.join(abs_path_out_folder, f"{base}_combined.py")
    with open(abs_path_combined_py, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    # try to compile the combined content to check for syntax errors
    try:
        compile(combined_content, f"{base}_combined.py", 'exec')
    except SyntaxError as e:
        with open(os.path.join(abs_path_out_folder, f"{base}_syntax_error.txt"), 'w', encoding='utf-8') as f:
            f.write(str(e))
        return  # skip the rest if syntax error
    # set config.json
    config = {
        "output_path": abs_path_out_folder,
        "obj_name": base
    }
    with open(config_json, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    # call blender
    command = [BLENDER_EXE, BLEND_FILE, "-P", abs_path_combined_py]  # opengl needs non-background mode
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    # log stdout and stderr to separate files if they are not None
    if result.stdout:
        stdout_log = os.path.join(abs_path_out_folder, f"{base}_blender_stdout.log")
        with open(stdout_log, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
    
    if result.stderr:
        stderr_log = os.path.join(abs_path_out_folder, f"{base}_blender_stderr.log")
        with open(stderr_log, 'w', encoding='utf-8') as f:
            f.write(result.stderr)

def combine_and_run_looped(abs_path_py: str, abs_path_out_folder: str, 
                            suffix_py: str=SUFFIX_PY, config_json: str=CONFIG_JSON):
    '''
    abs_path_py: absolute path to the py file to be combined
    abs_path_out_folder: absolute path to the output folder

    To support visual feedback loops: prefix every file write with iteration number
    if iteration is 0, then it's the first run; otherwise, get previous results accordingly
    '''
    base = os.path.basename(abs_path_py).split('.')[0]  # base is iteration already
    os.makedirs(abs_path_out_folder, exist_ok=True)
    # Read and combine files
    with open(abs_path_py, 'r', encoding='utf-8') as f1, open(suffix_py, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
    # add a try except block to content1 (src llm shape script)
    import_line = "import sys\nimport traceback\n"
    flag0_line = "success = True\n"
    try_line = "try:\n"
    except_line = "except Exception as e:\n"
    print_line = "    print('An error occurred:', file=sys.stderr)\n"
    traceback_line = "    traceback.print_exc(file=sys.stderr)\n"
    flush_line = "    sys.stderr.flush()  # Ensure that the error output is flushed\n"
    flag1_line = "    success = False\n"
    blender_quit_line = "    bpy.ops.wm.quit_blender()\n"  # somehow either of blender quit or python quit can't solve the problem
    everyline_tab = "    "
    content1 = import_line + flag0_line + try_line + everyline_tab + content1.replace('\n', '\n' + everyline_tab) + '\n' + except_line + print_line + traceback_line + flush_line + flag1_line + blender_quit_line
    combined_content = content1 + "\n" + content2
    abs_path_combined_py = os.path.join(abs_path_out_folder, f"{base}_combined.py")  # e.g. 0_combined.py
    with open(abs_path_combined_py, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    # try to compile the combined content to check for syntax errors
    try:
        compile(combined_content, f"{base}_combined.py", 'exec')
    except SyntaxError as e:
        with open(os.path.join(abs_path_out_folder, f"{base}_syntax_error.txt"), 'w', encoding='utf-8') as f:
            f.write(str(e))
        return  # skip the rest if syntax error
    # set config.json
    config = {
        "output_path": abs_path_out_folder,
        "obj_name": base  # now obj_name is iteration num too
    }
    with open(config_json, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    # call blender
    command = [BLENDER_EXE, BLEND_FILE, "-P", abs_path_combined_py]  # opengl needs non-background mode
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    # log stdout and stderr to separate files if they are not None
    if result.stdout:
        stdout_log = os.path.join(abs_path_out_folder, f"{base}_blender_stdout.log")
        with open(stdout_log, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
    
    if result.stderr:
        stderr_log = os.path.join(abs_path_out_folder, f"{base}_blender_stderr.log")
        with open(stderr_log, 'w', encoding='utf-8') as f:
            f.write(result.stderr)

def run_stl_render(stl_py_file=STL_PYFILE):
    command = [BLENDER_EXE, BLEND_FILE, "-P", stl_py_file]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    # stable process, record incremental logs locally
    # if result.stderr:  # record no log for now
    #     stderr_log = os.path.join(os.path.dirname(stl_py_file), "blender_stderr.log")
    #     with open(stderr_log, 'a', encoding='utf-8') as f:
    #         filtered_stderr = "\n".join(line for line in result.stderr.splitlines() if not (line.startswith("TBBmalloc") or line.startswith("Writing to")))
    #         f.write(filtered_stderr)

if __name__ == "__main__":
    # combine_and_run(
    #     exp_id="exp_a",
    #     output_py="sample_output.py"
    # )
    run_stl_render()
