import bpy
import math
from mathutils import Vector

def create_star_prism(radius, height, points):
    # Create the star base
    star_points = []
    for i in range(points * 2):
        angle = math.pi * i / points
        r = radius if i % 2 == 0 else radius / 2
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        star_points.append((x, y, 0))

    # Create the mesh
    mesh = bpy.data.meshes.new("StarPrism")
    obj = bpy.data.objects.new("StarPrism", mesh)

    bpy.context.collection.objects.link(obj)

    # Create geometry
    vertices = star_points + [(x, y, height) for x, y, z in star_points]
    faces = []

    # Create bottom face
    bottom_face = [i for i in range(points * 2)]
    faces.append(bottom_face)

    # Create side faces
    for i in range(points * 2):
        next_index = (i + 1) % (points * 2)
        faces.append([i, next_index, next_index + points * 2, i + points * 2])

    # Create top face
    top_face = [i + points * 2 for i in range(points * 2)]
    faces.append(top_face)

    # Create mesh from vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

create_star_prism(6, 10, 8)
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