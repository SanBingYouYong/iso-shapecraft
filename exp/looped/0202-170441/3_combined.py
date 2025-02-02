import sys
import traceback
success = True
try:
    import bpy
    import bmesh
    import math
    
    def create_wedge(length, width, height):
        # Create a new mesh and a new object
        mesh = bpy.data.meshes.new("Wedge")
        obj = bpy.data.objects.new("Wedge", mesh)
    
        # Link the object to the current collection
        bpy.context.collection.objects.link(obj)
    
        # Create a bmesh to define the shape
        bm = bmesh.new()
    
        # Define the vertices of the wedge
        v1 = bm.verts.new((0, 0, 0))  # Bottom left
        v2 = bm.verts.new((length, 0, 0))  # Bottom right
        v3 = bm.verts.new((length, width, 0))  # Top right
        v4 = bm.verts.new((0, width, 0))  # Top left
    
        # Create additional vertices for a smoother tapered end
        taper_height = height * 1.2
        num_taper_vertices = 8  # Number of vertices around the tapered top
        for i in range(num_taper_vertices):
            angle = (math.pi / (num_taper_vertices - 1)) * i  # Distribute vertices in a circular manner
            x = (length * 0.5) + (0.3 * math.cos(angle))  # Adjust radius for curvature
            y = (width * 0.5) + (0.3 * math.sin(angle))
            z = taper_height
            bm.verts.new((x, y, z))
    
        # Create faces for the bottom
        bm.faces.new((v1, v2, v3, v4))  # Bottom face
    
        # Create side faces
        taper_verts = list(bm.verts)[4:]  # Get the newly created taper vertices
        for i in range(len(taper_verts)):
            v_start = taper_verts[i]
            v_end = taper_verts[(i + 1) % len(taper_verts)]  # Wrap around
            bm.faces.new((v1, v2, v_start))  # Bottom faces to taper
            bm.faces.new((v2, v3, v_end))
            bm.faces.new((v3, v4, v_start))
            bm.faces.new((v4, v1, v_end))
    
        # Finish up and write the bmesh to the mesh
        bm.to_mesh(mesh)
        bm.free()
    
        # Recalculate normals for smooth shading
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()
    
    create_wedge(2, 1, 0.5)
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