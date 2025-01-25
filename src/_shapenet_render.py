import bpy
import os
import sys
import argparse


'''
This script is used to render the 3D models in the ShapeNet dataset to PNG images.
'''

def main(obj_dataset_path, output_folder):
    first_level_folders = os.listdir(obj_dataset_path)
    for first_level_folder in first_level_folders:
        second_level_folders = os.listdir(os.path.join(obj_dataset_path, first_level_folder))
        for second_level_folder in second_level_folders:
            obj_path = os.path.join(obj_dataset_path, first_level_folder, second_level_folder, "models", "model_normalized.obj")
            output_path = os.path.join(output_folder, first_level_folder, f"{second_level_folder}.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            load_render_delete(obj_path, output_path)

def load_render_delete(obj_path, output_path):
    bpy.ops.wm.obj_import(filepath=obj_path)
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['model_normalized'].select_set(True)
    bpy.ops.object.delete()

if __name__ == "__main__":
    print(f"Commencing rendering with {sys.argv}")
    args = sys.argv[sys.argv.index("--") + 1:]
    obj_dataset_path, output_folder = args
    main(obj_dataset_path, output_folder)

