import bpy

def create_cylinder(radius, depth):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(0, 0, 0))

create_cylinder(radius=1, depth=2)