import bpy

def create_icosahedron():
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=0, radius=1, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "Icosahedron"

create_icosahedron()