import sys
import traceback
success = True
try:
    import bpy
    
    def create_shopping_bag():
        # Create the bag body
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        bag = bpy.context.object
        bag.scale[0] = 0.6  # Width
        bag.scale[1] = 0.4  # Depth
        bag.scale[2] = 1.2  # Height (increased for more volume)
    
        # Go to edit mode to modify the shape
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Select the top face and scale it to create a tapered effect
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_face_by_sides(number=4, extend=False)  # Select the top face
        bpy.ops.transform.resize(value=(0.8, 0.8, 1))  # Slightly scale down the top face
    
        # Go back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
    
        # Create the handles
        handle_width = 0.2  # Increased width for sturdiness
        handle_length = 0.6  # Increased length for a better representation
        handle_height = 0.3  # Increased height for a robust look
    
        # Create left handle
        bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(-0.45, 0, 1.1))
        left_handle = bpy.context.object
        left_handle.rotation_euler[0] = 1.57  # Rotate to vertical
    
        # Create right handle
        bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(0.45, 0, 1.1))
        right_handle = bpy.context.object
        right_handle.rotation_euler[0] = 1.57  # Rotate to vertical
    
        # Position handles correctly
        left_handle.location.z += handle_height / 2
        right_handle.location.z += handle_height / 2
    
        # Create a defined base for the bag
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -0.1))
        base = bpy.context.object
        base.scale[0] = 0.65  # Slightly wider than the bag
        base.scale[1] = 0.45  # Slightly deeper than the bag
        base.scale[2] = 0.1   # Thin base for realistic appearance
    
        # Join the bag and handles and base
        bpy.ops.object.select_all(action='DESELECT')
        bag.select_set(True)
        left_handle.select_set(True)
        right_handle.select_set(True)
        base.select_set(True)
        bpy.context.view_layer.objects.active = bag
        bpy.ops.object.join()
    
    create_shopping_bag()
except Exception as e:
    print('An error occurred:', file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()  # Ensure that the error output is flushed
    success = False
    bpy.ops.wm.quit_blender()

if not success:
    print("An error occurred during shape script execution, see error log for details; skipping rendering and exporting.")
    sys.exit(1)
import json
import os
import random
random.seed(0)  # for reproducibility, remove before production
# bpy would have been imported in previous code
CONFIG_FILEPATH = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\config.json"
with open(CONFIG_FILEPATH, 'r') as f:
    config = json.load(f)
output_path = config["output_path"]  # e.g. absolute path to exp/...
obj_name = config["obj_name"]  # e.g. an id
print(f"Output path: {output_path}")
print(f"Object name: {obj_name}")
# render_out = os.path.join(output_path, f"render\\{obj_name}.png")
render_out = os.path.join(output_path, f"{obj_name}.png")  # multi-view renders handle this properly already

obj_out = os.path.join(output_path, f"obj\\{obj_name}.obj")  # this will only be one obj
obj_out = os.path.join(output_path, f"{obj_name}.obj")  # this will only be one obj
print(f"Rendering to {render_out}")
print(f"Exporting to {obj_out}")


def select_objects_join_normalize_size(collection: str="Collection"):
    """
    Select all objects in the collection, join them, and normalize the size
    """
    collection = bpy.data.collections[collection]
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        if obj.name in ["Camera", "Light", "Empty"]:
            continue
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj = bpy.context.object
    bbox = obj.bound_box
    min_x = min([coord[0] for coord in bbox])
    max_x = max([coord[0] for coord in bbox])
    min_y = min([coord[1] for coord in bbox])
    max_y = max([coord[1] for coord in bbox])
    min_z = min([coord[2] for coord in bbox])
    max_z = max([coord[2] for coord in bbox])

    scale_x = 2 / (max_x - min_x) if max_x != min_x else 1
    scale_y = 2 / (max_y - min_y) if max_y != min_y else 1
    scale_z = 2 / (max_z - min_z) if max_z != min_z else 1
    scale = min(scale_x, scale_y, scale_z)

    bpy.ops.transform.resize(value=(scale, scale, scale))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.location_clear()

def export_obj(path):
    # assumption: obj has been selected by above method
    # obj = bpy.context.object
    # bpy.ops.object.select_all(action='DESELECT')
    # obj.select_set(True)
    bpy.ops.wm.obj_export(filepath=path)

select_objects_join_normalize_size()

# bpy.context.scene.render.filepath = render_out
# bpy.ops.render.render(write_still=True)

def set_camera(camera, x, y, z=1.5):
    """
    Camera is tracked to [0, 0, 0] by default, so only change its x y z coordinates
    """
    camera.location.x = x
    camera.location.y = y
    camera.location.z = z

base_cam_pos = [
        [2.8, -2.8, 1.5],
        [2.8, 2.8, 1.5],
        [-2.8, 2.8, 1.5],
        [-2.8, -2.8, 1.5]
    ]

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

multi_view_render(render_out)

export_obj(obj_out)

# quit blender if not in background mode
# if bpy.context.space_data is not None:
if not bpy.app.background:
    bpy.ops.wm.quit_blender()