import bpy
import math

def create_twisted_torus(minor_radius, major_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, align='WORLD', location=(0, 0, 0))
    torus = bpy.context.active_object
    
    # Twist the torus
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    torus.rotation_euler[2] = math.radians(twist_angle)

# Parameters
minor_radius = 3
major_radius = 10
twist_angle = 45

create_twisted_torus(minor_radius, major_radius, twist_angle)