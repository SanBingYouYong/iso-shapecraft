import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), 
                                      major_radius=major_radius, 
                                      minor_radius=minor_radius)
    torus = bpy.context.object
    
    # Apply rotation for twist
    torus.rotation_euler[0] = math.radians(twist_angle)

create_twisted_torus(10, 3, 45)