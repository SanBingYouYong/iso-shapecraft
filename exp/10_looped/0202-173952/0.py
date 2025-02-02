import bpy

def create_shoe_box(length, width, height):
    bpy.ops.mesh.primitive_cube_add(size=1)
    shoe_box = bpy.context.object
    shoe_box.scale = (length / 2, width / 2, height / 2)
    shoe_box.location = (0, 0, height / 2)

create_shoe_box(2, 1, 0.5)