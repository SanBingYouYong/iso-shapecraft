import bpy

def create_sphere(radius=1, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)

create_sphere()