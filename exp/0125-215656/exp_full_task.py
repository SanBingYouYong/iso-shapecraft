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