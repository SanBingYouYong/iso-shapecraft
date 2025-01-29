import bpy
import bmesh
from math import radians

def create_diamond(size):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Diamond")
    obj = bpy.data.objects.new("Diamond", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the diamond shape
    bm = bmesh.new()

    # Define the vertices of the diamond
    verts = [
        bm.verts.new((0, 0, size)),   # Top vertex
        bm.verts.new((size, 0, 0)),   # Right vertex
        bm.verts.new((0, -size, 0)),  # Bottom vertex
        bm.verts.new((-size, 0, 0)),  # Left vertex
    ]

    # Create the faces of the diamond
    bmesh.ops.edge_face(bm, edges=bm.edges[:], verts=verts)

    # Finish up and write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Move the object to the center
    obj.location = (0, 0, 0)

# Create the diamond shape with a specified size
create_diamond(1)