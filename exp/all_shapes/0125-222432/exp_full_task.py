import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, 
                                      location=(0, 0, 0), rotation=(0, 0, 0))
    torus = bpy.context.object
    
    # Apply a twist along the Z axis
    for vertex in torus.data.vertices:
        angle = twist_angle * (vertex.co.z / (2 * math.pi * major_radius))
        x = vertex.co.x * math.cos(angle) - vertex.co.y * math.sin(angle)
        y = vertex.co.x * math.sin(angle) + vertex.co.y * math.cos(angle)
        vertex.co.x = x
        vertex.co.y = y

create_twisted_torus(10, 3, math.radians(45))