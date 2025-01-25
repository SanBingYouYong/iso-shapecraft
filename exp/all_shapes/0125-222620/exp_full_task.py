import bpy

def create_beveled_cube(edge_length=10, bevel_radius=1):
    bpy.ops.mesh.primitive_cube_add(size=edge_length)
    cube = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=bevel_radius, segments=10)
    bpy.ops.object.mode_set(mode='OBJECT')

create_beveled_cube()