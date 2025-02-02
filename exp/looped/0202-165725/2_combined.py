import sys
import traceback
success = True
try:
    import bpy
    import bmesh
    from mathutils import Vector
    
    def create_smooth_tapered_wedge(length=2.0, width=1.0, height=1.0, taper_amount=0.3, subdivisions=3):
        # Create a new mesh and object
        mesh = bpy.data.meshes.new("SmoothTaperedWedge")
        obj = bpy.data.objects.new("SmoothTaperedWedge", mesh)
    
        # Link the object to the scene
        bpy.context.collection.objects.link(obj)
    
        # Create the mesh data
        bm = bmesh.new()
    
        # Define vertices for a more pronounced tapered wedge shape
        v1 = bm.verts.new((0, 0, 0))  # Base back left
        v2 = bm.verts.new((length, 0, 0))  # Base back right
        v3 = bm.verts.new((length, width, 0))  # Base front right
        v4 = bm.verts.new((0, width, 0))  # Base front left
    
        # Add more subdivided vertices to enhance smoothness on the tapered end
        for i in range(subdivisions + 1):
            t = i / subdivisions
            bm.verts.new((length * (1 - t * taper_amount), 0, height * t))  # Back edge
            bm.verts.new((length * (1 - t * taper_amount), width, height * t))  # Front edge
        
        # Collect all the new vertices for easier access
        new_verts = list(bm.verts)[4:]  # Skip the first four base vertices
    
        # Create faces for the tapered wedge
        bm.faces.new((v1, v2, new_verts[0], new_verts[1]))  # Back face
        bm.faces.new((v2, v3, new_verts[-1], new_verts[-2]))  # Right face
        bm.faces.new((v3, v4, new_verts[3], new_verts[2]))  # Front face
        bm.faces.new((v4, v1, new_verts[1], new_verts[0]))  # Left face
        
        # Side faces connecting to the top
        for i in range(1, len(new_verts) - 1):
            bm.faces.new((new_verts[i - 1], new_verts[i], new_verts[i + 1], new_verts[i + len(new_verts) // 2]))
    
        # Finish the mesh
        bm.to_mesh(mesh)
        bm.free()
    
        # Smooth the shading
        for face in mesh.polygons:
            face.use_smooth = True
    
        # Set the origin to the center of the geometry
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    
    create_smooth_tapered_wedge()
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