import bpy
import math

def create_twisted_torus(minor_radius, major_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, location=(0, 0, 0))
    
    # Get the created torus object
    torus = bpy.context.object
    
    # Apply rotation to twist the torus
    torus.rotation_euler[2] = math.radians(twist_angle)

# Parameters for the torus
minor_radius = 3
major_radius = 10
twist_angle = 45

create_twisted_torus(minor_radius, major_radius, twist_angle)