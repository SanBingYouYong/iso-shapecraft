import bpy

def create_cube(size=1):
    bpy.ops.mesh.primitive_cube_add(size=size)

create_cube()