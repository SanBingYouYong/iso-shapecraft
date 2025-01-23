import subprocess


'''
Script to call Blender and execute some python script. 
'''

# Path to the Blender executable
blender_executable = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe"

# Path to the Blender script you want to execute
blender_script = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\src\\auto_render.py"
# output_path = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\outputs\\test.png"
# obj_filepath = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapenetcore_select\\02747177\\1d3a7ed6ff0dfc9e63b2acb037dfbcde\\models\\model_normalized.obj"
# obj_dataset = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapenetcore_select"
obj_dataset = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapenet_test"
output_folder = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\outputs"

# Path to the blank blend file
# blank_blend_file = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\blank42.blend"
render_blend_file = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\shapenet_render.blend"

# Command to call Blender and execute the script with the blank blend file
command = [blender_executable, "-b", render_blend_file, "-P", blender_script, "--", obj_dataset, output_folder]

# Execute the command
subprocess.run(command)