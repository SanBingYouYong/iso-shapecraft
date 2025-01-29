import bpy
import bmesh

def create_hexagonal_prism(edge_length=5, height=15):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrismMesh")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the vertices for a hexagonal prism
    half_edge = edge_length / 2
    vertices = [
        (half_edge * 1.0, 0, 0),
        (half_edge * 0.5, half_edge * 1.732, 0),
        (-half_edge * 0.5, half_edge * 1.732, 0),
        (-half_edge * 1.0, 0, 0),
        (-half_edge * 0.5, -half_edge * 1.732, 0),
        (half_edge * 0.5, -half_edge * 1.732, 0),
        (half_edge * 1.0, 0, height),
        (half_edge * 0.5, half_edge * 1.732, height),
        (-half_edge * 0.5, half_edge * 1.732, height),
        (-half_edge * 1.0, 0, height),
        (-half_edge * 0.5, -half_edge * 1.732, height),
        (half_edge * 0.5, -half_edge * 1.732, height),
    ]

    # Create vertices in bmesh
    verts = [bm.verts.new(v) for v in vertices]

    # Create faces for the top and bottom
    bm.faces.new(verts[0:6])  # Bottom face
    bm.faces.new(verts[6:12]) # Top face

    # Create side faces
    for i in range(6):
        bm.faces.new((verts[i], verts[(i + 1) % 6], verts[(i + 1) % 6 + 6], verts[i + 6]))

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

create_hexagonal_prism()
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