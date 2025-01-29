import bpy

def create_octahedron():
    bpy.ops.mesh.primitive_octahedron_add(size=1, location=(0, 0, 0))

create_octahedron()