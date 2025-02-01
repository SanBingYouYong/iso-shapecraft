import sys
import traceback
success = True
try:
    import bpy
    import math
    
    def create_pie_slice(radius=1, angle=90, location=(0, 0, 0)):
        bpy.ops.object.select_all(action='DESELECT')
        
        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name="PieSlice")
        obj = bpy.data.objects.new("PieSlice", mesh)
        
        # Link the object to the collection
        bpy.context.collection.objects.link(obj)
        
        # Create the geometry of the pie slice
        verts = [(0, 0, 0)]  # Center vertex
        edges = []
        faces = []
    
        # Calculate the number of segments based on the angle
        num_segments = 32  # More segments for a smoother curve
        segment_angle = math.radians(angle / num_segments)
    
        for i in range(num_segments + 1):
            theta = i * segment_angle
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            verts.append((x, y, 0))
    
            if i > 0:
                edges.append((0, i))  # Connect center to outer vertices
                if i < num_segments:
                    faces.append((0, i, i + 1))  # Create face with center and two outer vertices
    
        # Create the mesh from the gathered vertices, edges, and faces
        mesh.from_pydata(verts, edges, faces)
        mesh.update()
    
        # Move the object to the desired location
        obj.location = location
    
        # Set the object as active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
    
    create_pie_slice()
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