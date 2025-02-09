import bpy
import json
import os
from mathutils import Vector
import random

CONFIG_FILEPATH = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\stl_config.json"
base_cam_pos = [
        [2.8, -2.8, 1.5],
        [2.8, 2.8, 1.5],
        [-2.8, 2.8, 1.5],
        [-2.8, -2.8, 1.5]
    ]

def load_config(config_path=CONFIG_FILEPATH):
    with open(config_path, "r") as f:
        return json.load(f)

def import_stl(stl_path):
    # somehow bpy.ops.import_mesh.stl could not be found, must've been an API update
    bpy.ops.wm.stl_import(filepath=stl_path)
    return bpy.context.selected_objects[0]

def normalize_object(obj):
    # Compute object bounding box dimensions
    min_corner = Vector(obj.bound_box[0]) @ obj.matrix_world
    max_corner = Vector(obj.bound_box[6]) @ obj.matrix_world
    size = max_corner - min_corner
    
    # Scale object to fit within unit cube
    max_dim = max(size)
    if max_dim > 0:
        scale_factor = 1.0 / max_dim
        obj.scale *= scale_factor
        bpy.ops.object.transform_apply(scale=True)
    
    # Compute the new bounding box center
    min_corner = Vector(obj.bound_box[0]) @ obj.matrix_world
    max_corner = Vector(obj.bound_box[6]) @ obj.matrix_world
    center = (min_corner + max_corner) / 2
    
    # Translate object to center it at (0, 0, 0)
    obj.location -= center
    bpy.ops.object.transform_apply(location=True)

def export_obj(obj, path):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.wm.obj_export(filepath=path)

def render(output_path):
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

def set_camera(camera, x, y, z=1.5):
    """
    Camera is tracked to [0, 0, 0] by default, so only change its x y z coordinates
    """
    camera.location.x = x
    camera.location.y = y
    camera.location.z = z

def multi_view_render(filepath: str, views=base_cam_pos, rand_offset=0.3):
    """
    Render the current scene from multiple views. 

    filepath: the path to save the rendered images. with or without .png suffix
    views: list of camera positions, e.g. [[2.8, -2.8, 1.5], [2.8, 2.8, 1.5], [-2.8, 2.8, 1.5], [-2.8, -2.8, 1.5]] to be sampled from.
        by default we also apply random offset to each coord based on rand_offset
    """
    # camera already locks onto 000
    filepath = filepath if not filepath.endswith(".png") else filepath[:-4]

    for i, view in enumerate(views):
        randoms = [random.uniform(-rand_offset, rand_offset) for _ in range(3)]
        cam_coord = [view[i] + randoms[i] for i in range(3)]
        camera = bpy.data.objects['Camera']
        set_camera(camera, *cam_coord)
        bpy.context.scene.render.filepath = filepath + f"_{i}.png"
        # bpy.ops.render.render(write_still=True)
        bpy.ops.render.opengl(write_still=True)  # to render objects with no volume/thickness...

def main():
    config = load_config()
    stl_path = config['stl_abspath']  # to be imported
    obj_name = config['obj_name']  # object's base name
    output_folder = config['out_abspath']  # path to a folder to store renders
    os.makedirs(output_folder, exist_ok=True)
    obj = import_stl(stl_path)
    normalize_object(obj)
    obj_out = os.path.join(output_folder, f"{obj_name}.obj")
    export_obj(obj, obj_out)
    render_out = os.path.join(output_folder, f"{obj_name}.png")
    multi_view_render(render_out)

    if not bpy.app.background:
        bpy.ops.wm.quit_blender()

if __name__ == "__main__":
    main()

