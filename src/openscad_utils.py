import subprocess
import os
import json


OPENSCAD_EXE = "C:\Program Files\OpenSCAD\openscad.exe"
STL_PYFILE = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\render_stl.py"
STL_JSON = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\stl_config.json"

BLENDER_EXE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe"
BLEND_FILE = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\auto_render.blend"


def _run_stl_render(stl_py_file=STL_PYFILE):
    command = [BLENDER_EXE, BLEND_FILE, "-P", stl_py_file]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    return result

def run_render_export(scad_abs_path: str, output_folder_abs_path: str):
    no_error = run_openscad(scad_abs_path, output_folder_abs_path)
    if not no_error:
        # print(f"An error processing {scad_abs_path}, check {output_folder_abs_path} for logs.")
        return
    stl_abs_path = os.path.join(output_folder_abs_path, os.path.basename(scad_abs_path).split(".")[0] + ".stl")
    config = {
        "stl_abspath": stl_abs_path,
        "obj_name": os.path.basename(scad_abs_path).split(".")[0],
        "out_abspath": output_folder_abs_path
    }
    with open(STL_JSON, "w") as f:
        json.dump(config, f)
    result = _run_stl_render()
    if result.stderr:
        log_file = os.path.join(output_folder_abs_path, "render_log.txt")
        filtered_stderr = [line for line in result.stderr.splitlines() if not (line.startswith("TBBmalloc") or line.startswith("Writing to"))]
        if filtered_stderr != []:
            with open(log_file, "w") as f:
                f.write("\n".join(filtered_stderr))


def run_openscad(scad_abs_path: str, output_folder_abs_path: str):
    '''
    Wrapper for _run_openscad that checks if the SCAD file exists and creates the output folder if it doesn't exist.
    Outputs use the same basename as the SCAD file.
    '''
    if not os.path.exists(scad_abs_path):
        raise FileNotFoundError(f"SCAD file not found: {scad_abs_path}")
    os.makedirs(output_folder_abs_path, exist_ok=True)
    scad_base = os.path.basename(scad_abs_path).split(".")[0]
    model_filename = f"{scad_base}.stl"
    image_filename = f"{scad_base}.png"
    error_log_filename = f"{scad_base}.log"
    return _run_openscad(
        scad_abs_path,
        output_folder_abs_path,
        model_filename=model_filename,
        image_filename=image_filename,
        error_log_filename=error_log_filename,
        openscad_executable=OPENSCAD_EXE
    )

def _log_error(error_log_path: str, errors: list):
    with open(error_log_path, "w") as f:
        f.write("\n\n".join(errors))

def _run_openscad(scad_file, output_folder,
                 model_filename="output.stl", image_filename="output.png",
                 error_log_filename="error_log.txt",
                 openscad_executable=OPENSCAD_EXE):
    """
    Runs OpenSCAD to generate a 3D model and a rendered image from the given .scad file.
    If errors occur (e.g., syntax errors in the .scad file), they are captured and written to a log file.
    
    Parameters:
        scad_file (str): Path to the input .scad file.
        output_folder (str): Directory where the generated files and error log will be saved.
        model_filename (str): Filename for the exported 3D model (default "output.stl").
        image_filename (str): Filename for the exported rendered image (default "output.png").
        error_log_filename (str): Filename for the error log (default "error_log.txt").
        openscad_executable (str): Path to the OpenSCAD executable (default "openscad").
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    error_log_path = os.path.join(output_folder, error_log_filename)
    # Remove any previous error log
    if os.path.exists(error_log_path):
        os.remove(error_log_path)
    
    errors = []  # List to collect error messages

    # Construct full paths for the output files
    model_output_path = os.path.join(output_folder, model_filename)
    # image_output_path = os.path.join(output_folder, image_filename)
    
    # Command to export the 3D model (e.g., STL file)
    cmd_model = [
        openscad_executable,
        "-o", model_output_path,
        scad_file
    ]
    
    # Command to export the rendered image
    # You can adjust options like --imgsize, --camera, or --render as needed.
    # cmd_image = [
    #     openscad_executable,
    #     "--imgsize=256,256",
    #     "-o", image_output_path,
    #     scad_file
    # ]
    
    # Run the command for exporting the 3D model
    try:
        # print("Running OpenSCAD for 3D model export...")
        result_model = subprocess.run(cmd_model, capture_output=True, text=True, check=False)
        if result_model.returncode != 0:
            errors.append("Error exporting 3D model:\n" + result_model.stderr)
            _log_error(error_log_path, errors)
            return
    except Exception as e:
        errors.append("Exception during 3D model export: " + str(e))
        _log_error(error_log_path, errors)
        return
    
    # Check if the model file was created
    if not os.path.exists(model_output_path):
        errors.append(f"3D model output file not found: {model_output_path}")
        _log_error(error_log_path, errors)
        return
    
    # Run the command for exporting the rendered image  # now we rely on blender renders
    # try:
    #     # print("Running OpenSCAD for image export...")
    #     result_image = subprocess.run(cmd_image, capture_output=True, text=True, check=False)
    #     if result_image.returncode != 0:
    #         errors.append("Error exporting rendered image:\n" + result_image.stderr)
    #         _log_error(error_log_path, errors)
    #         return
    # except Exception as e:
    #     errors.append("Exception during image export: " + str(e))
    #     _log_error(error_log_path, errors)
    #     return
    
    # # Check if the image file was created
    # if not os.path.exists(image_output_path):
    #     errors.append(f"Rendered image file not found: {image_output_path}")
    #     _log_error(error_log_path, errors)
    #     return
    
    # If any errors occurred, write them to the error log file
    if errors != []:
        print(f"Operation completed with errors. See {error_log_path} for details.")
        with open(error_log_path, "w") as f:
            f.write("\n\n".join(errors))
        # print(f"Operation completed with errors. See {error_log_path} for details.")
    else:
        # print("Operation completed successfully.")
        pass

    return errors == []

# Example usage:
if __name__ == "__main__":
    # scad_file_path = "bottle.scad"
    # output_dir = "exp/scads"
    # _run_openscad(scad_file_path, output_dir)
    run_render_export("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scads_full\coffee_mug\\sub_task_0\\0_0.scad", "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scads_full\coffee_mug\\sub_task_0")
