import bpy
import bmesh
from math import radians

def create_arch(radius=1, height=1, segments=16):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Arch")
    obj = bpy.data.objects.new("Arch", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the arch
    bm = bmesh.new()

    for i in range(segments + 1):
        angle = radians(180 * (i / segments))
        x = radius * (1 - (angle / (radians(180))))  # X position
        y = radius * -1 * (1 - (angle / (radians(180))))  # Y position
        z = height * (1 - (i / segments))  # Z position
        bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, segments=segments, location=(x, y, z))

    # Create the mesh from the bmesh
    bm.to_mesh(mesh)
    bm.free()

create_arch()