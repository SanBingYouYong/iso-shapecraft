import bpy
import bmesh
from math import radians

def create_hexagonal_prism(edge_length=5, height=15):
    # Create a new mesh
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh for the hexagonal prism
    bm = bmesh.new()
    
    # Calculate the vertices of the hexagon
    vertices = []
    for i in range(6):
        angle = radians(60 * i)
        x = edge_length * cos(angle)
        y = edge_length * sin(angle)
        vertices.append((x, y, 0))  # Base vertices
        vertices.append((x, y, height))  # Top vertices

    # Create the vertices in the bmesh
    verts = [bm.verts.new(v) for v in vertices]
    bm.verts.ensure_lookup_table()
    
    # Create faces for the base and top
    bm.faces.new(verts[:6])  # Base face
    bm.faces.new(verts[6:])  # Top face
    
    # Create side faces
    for i in range(6):
        bm.faces.new((verts[i], verts[(i + 1) % 6], verts[(i + 1) % 6 + 6], verts[i + 6]))
    
    # Finish the bmesh and update the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set shading to smooth
    bpy.ops.object.shade_smooth()
    
create_hexagonal_prism()import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, location=(0, 0, 0))
    torus = bpy.context.object

    # Apply the twist
    bpy.ops.object.select_all(action='DESELECT')
    torus.select_set(True)
    bpy.context.view_layer.objects.active = torus
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Rotate the torus around the Z axis to create the twist
    torus.rotation_euler[2] += math.radians(twist_angle)

# Create a torus with specified parameters
create_twisted_torus(major_radius=10, minor_radius=3, twist_angle=45)import bpy

def create_concentric_spheres():
    radii = [2, 4, 6]
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue

    for i, radius in enumerate(radii):
        # Create a new sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.object
        
        # Create a new material
        material = bpy.data.materials.new(name=f"Material_{i}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = colors[i]  # Set color
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        
        # Assign the material to the sphere
        if sphere.data.materials:
            sphere.data.materials[0] = material
        else:
            sphere.data.materials.append(material)

create_concentric_spheres()
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