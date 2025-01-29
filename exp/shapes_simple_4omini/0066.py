import bpy
import bmesh
from math import radians

def create_kite_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Kite")
    obj = bpy.data.objects.new("Kite", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a BMesh for geometry creation
    bm = bmesh.new()

    # Define the vertices of the kite shape
    v1 = bm.verts.new((0, 0, 1))  # Top vertex
    v2 = bm.verts.new((1, 0, 0))  # Right vertex
    v3 = bm.verts.new((0, 1, 0))  # Bottom vertex
    v4 = bm.verts.new((-1, 0, 0)) # Left vertex
    v5 = bm.verts.new((0, 0, -1)) # Bottom point

    # Create faces for the kite shape
    bm.faces.new((v1, v2, v3))
    bm.faces.new((v1, v3, v4))
    bm.faces.new((v1, v4, v5))
    bm.faces.new((v1, v5, v2))
    bm.faces.new((v2, v3, v5))
    bm.faces.new((v3, v4, v5))

    # Update mesh with the new geometry
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the kite shape
create_kite_shape()