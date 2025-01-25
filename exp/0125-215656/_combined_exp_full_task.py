import bpy
import bmesh

def create_hexagonal_prism(base_edge_length, height):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=base_edge_length, depth=height, location=(0, 0, height / 2))
    prism = bpy.context.object
    bpy.ops.object.shade_smooth()
    
    # Adjust the scale to form a prism (if necessary)
    prism.scale[2] = height / 2  # Ensure it is a prism, height is adjusted

create_hexagonal_prism(5, 15)import bpy
import math

def create_twisted_torus(minor_radius, major_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0))
    
    # Get the active object (the torus)
    torus = bpy.context.active_object
    
    # Apply a twist by rotating the torus around its axis
    torus.rotation_euler[0] += math.radians(twist_angle)

# Parameters for the torus
minor_radius = 3
major_radius = 10
twist_angle = 45

create_twisted_torus(minor_radius, major_radius, twist_angle)import bpy

def create_concentric_spheres():
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue
    radii = [2, 4, 6]
    
    for radius, color in zip(radii, colors):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius)
        sphere = bpy.context.object
        sphere.location = (0, 0, 0)

        # Create a material
        material = bpy.data.materials.new(name=f"Material_{radius}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        
        # Assign material to the sphere
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