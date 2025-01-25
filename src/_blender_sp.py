import subprocess
import time
from tqdm import tqdm
import os
import sys
import signal


'''
Script to call Blender and execute some python script. 
'''

# Params
blender_executable = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe"

blender_script = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\src\\_shapenet_render.py"
render_blend_file = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\shapenet_render.blend"

# obj_dataset = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapenet_test"
obj_dataset = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\dataset\\shapenetcore_select"
output_folder = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\outputs"

# Command to call Blender and execute the script
command = [blender_executable, "-b", render_blend_file, "-P", blender_script, "--", obj_dataset, output_folder]

log_file = f"./logs/renderlog_{time.strftime('%Y%m%d-%H%M%S')}.log"

# Start timer
start_time = time.time()

# Count the number of images to render
total_images = 0
for root, dirs, files in os.walk(obj_dataset):
    for file in files:
        if file.endswith(".obj"):
            total_images += 1

pbar = tqdm(total=total_images, desc="Rendering", unit="image")

# Handler for termination signals
def signal_handler(sig, frame):
    print("Terminating process...")
    process.terminate()
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Execute the command and capture output
with open(log_file, "w") as f:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        # Check if the line matches the saved pattern
        if line.startswith("Saved:"):
            # Update progress bar
            pbar.update(1)
        if not line.startswith("Fra"):
            # Write the output to the log file
            f.write(line)
        # Check if the process has terminated
        if process.poll() is not None:
            break

# Close progress bar
pbar.close()

# Calculate elapsed time
elapsed_time = time.time() - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")
print(f"Log file saved as: {log_file}")
