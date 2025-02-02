import sys
import traceback
success = True
try:
    import bpy
    import bmesh
    from mathutils import Vector
    
    def create_pizza_slice():
        # Parameters for the pizza slice
        radius = 1.0
        crust_thickness = 0.2
        slice_angle = 60  # degrees
        slice_height = 0.2
    
        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name="PizzaSlice")
        obj = bpy.data.objects.new("PizzaSlice", mesh)
        
        # Link the object to the scene
        bpy.context.collection.objects.link(obj)
    
        # Create a bmesh to build the geometry
        bm = bmesh.new()
    
        # Create the outer edge vertices (crust)
        outer_verts = []
        for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
            rad = (angle * 3.14159) / 180
            x = radius * Vector((1, 0, 0)).rotate(Vector((0, 0, rad)))
            outer_verts.append(bm.verts.new(x + Vector((0, 0, crust_thickness))))
    
        # Create the inner edge vertices (topping)
        inner_verts = []
        for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
            rad = (angle * 3.14159) / 180
            x = (radius - crust_thickness) * Vector((1, 0, 0)).rotate(Vector((0, 0, rad)))
            inner_verts.append(bm.verts.new(x))
    
        # Create faces for the pizza slice
        for i in range(len(outer_verts) - 1):
            bm.faces.new((outer_verts[i], outer_verts[i+1], inner_verts[i+1], inner_verts[i]))
    
        # Create the tip face
        bm.faces.new((inner_verts[0], inner_verts[-1], outer_verts[-1], outer_verts[0]))
    
        # Write the bmesh into the mesh
        bm.to_mesh(mesh)
        bm.free()
    
        # Move the pizza slice up to visualize it better
        obj.location.z += slice_height / 2
    
        # Select and set the object as active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
    
    create_pizza_slice()
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