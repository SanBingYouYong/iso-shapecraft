import bpy

def create_chair():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create chair legs
    leg_height = 1.0
    leg_radius = 0.05
    leg_offset = 0.4
    
    for x in [-leg_offset, leg_offset]:
        for y in [-leg_offset, leg_offset]:
            bpy.ops.mesh.primitive_cylinder_add(radius=leg_radius, depth=leg_height, location=(x, y, leg_height / 2))
    
    # Create seat
    seat_width = 0.8
    seat_depth = 0.8
    seat_height = 0.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, leg_height + seat_height / 2))
    seat = bpy.context.object
    seat.scale = (seat_width / 2, seat_depth / 2, seat_height / 2)

    # Create backrest
    backrest_width = seat_width
    backrest_height = 0.5
    backrest_thickness = 0.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -seat_depth / 2 - backrest_thickness / 2, leg_height + seat_height + backrest_height / 2))
    backrest = bpy.context.object
    backrest.scale = (backrest_width / 2, backrest_thickness / 2, backrest_height / 2)
    
    # Adjust backrest position for curvature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    backrest.data.vertices[0].co.z += 0.1  # Slightly raise the top vertex for curvature
    backrest.data.vertices[1].co.z += 0.1
    backrest.data.vertices[2].co.z -= 0.1
    backrest.data.vertices[3].co.z -= 0.1
    bpy.ops.object.mode_set(mode='OBJECT')

create_chair()
import json
import os
# bpy would have been imported in previous code
CONFIG_FILEPATH = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\config.json"
with open(CONFIG_FILEPATH, 'r') as f:
    config = json.load(f)
output_path = config["output_path"]  # e.g. absolute path to exp/...
obj_name = config["obj_name"]  # e.g. an id
print(f"Output path: {output_path}")
print(f"Object name: {obj_name}")
render_out = os.path.join(output_path, f"render\\{obj_name}.png")  # TODO: multi-view renders?
obj_out = os.path.join(output_path, f"obj\\{obj_name}.obj")  # this will only be one obj
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

    scale_x = 2 / (max_x - min_x)
    scale_y = 2 / (max_y - min_y)
    scale_z = 2 / (max_z - min_z)
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

bpy.context.scene.render.filepath = render_out
bpy.ops.render.render(write_still=True)

export_obj(obj_out)