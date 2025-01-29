import bpy

def create_cone(radius=1, depth=2, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=radius, depth=depth, location=location)

create_cone()