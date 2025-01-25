import bpy
import math

def create_twisted_torus(minor_radius, major_radius, twist_angle):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)

    # Create a torus
    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), 
                                      major_radius=major_radius, 
                                      minor_radius=minor_radius, 
                                      major_segments=48, 
                                      minor_segments=24)
    
    # Get the active object (the torus we just created)
    torus = bpy.context.active_object
    
    # Apply the twist along the z-axis
    bpy.ops.object.transform_apply(rotation=True)
    torus.rotation_euler[2] += math.radians(twist_angle)

# Parameters for the torus
minor_radius = 3
major_radius = 10
twist_angle = 45

create_twisted_torus(minor_radius, major_radius, twist_angle)