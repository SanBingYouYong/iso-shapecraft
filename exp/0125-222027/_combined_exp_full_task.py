import bpy
import bmesh
from mathutils import Vector

def create_hexagonal_prism(base_edge_length, height):
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create bmesh
    bm = bmesh.new()

    # Define the vertices for a hexagonal prism
    angle_offset = 360 / 6
    vertices = []
    for i in range(6):
        angle = math.radians(i * angle_offset)
        x = base_edge_length * math.cos(angle)
        y = base_edge_length * math.sin(angle)
        vertices.append(Vector((x, y, 0)))
        vertices.append(Vector((x, y, height)))

    # Create vertices in bmesh
    for v in vertices:
        bm.verts.new(v)
    
    bm.verts.ensure_lookup_table()

    # Create faces for the sides of the prism
    for i in range(6):
        v1 = bm.verts[i]
        v2 = bm.verts[(i + 1) % 6]
        v3 = bm.verts[(i + 1) % 6 + 6]
        v4 = bm.verts[i + 6]
        bm.faces.new((v1, v2, v3, v4))
    
    # Create top and bottom faces
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]))  # Bottom face
    bm.faces.new((bm.verts[6], bm.verts[7], bm.verts[5], bm.verts[4]))  # Top face

    # Finalize the bmesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function with specified dimensions
create_hexagonal_prism(base_edge_length=5, height=15)
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