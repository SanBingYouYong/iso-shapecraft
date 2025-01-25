import bpy
import bmesh

def create_square_based_pyramid(base_length, height, top_height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("SquareBasedPyramid")
    obj = bpy.data.objects.new("SquareBasedPyramid", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh object
    bm = bmesh.new()

    # Define the vertices
    half_base = base_length / 2
    vertices = [
        (-half_base, -half_base, 0),  # Vertex 0
        (half_base, -half_base, 0),   # Vertex 1
        (half_base, half_base, 0),    # Vertex 2
        (-half_base, half_base, 0),   # Vertex 3
        (0, 0, top_height)             # Vertex 4 (top vertex)
    ]

    # Add vertices to bmesh
    for v in vertices:
        bm.verts.new(v)

    # Ensure the bmesh updates
    bm.verts.ensure_lookup_table()

    # Create faces (base and four triangular sides)
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3]))  # Base face
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[4]))  # Side face 1
    bm.faces.new((bm.verts[1], bm.verts[2], bm.verts[4]))  # Side face 2
    bm.faces.new((bm.verts[2], bm.verts[3], bm.verts[4]))  # Side face 3
    bm.faces.new((bm.verts[3], bm.verts[0], bm.verts[4]))  # Side face 4

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set object properties
    obj.location = (0, 0, height / 2)

# Parameters for the pyramid
base_length = 8
height = 12
top_height = 9

create_square_based_pyramid(base_length, height, top_height)
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