import bpy
import bmesh
from math import radians

def create_diamond():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Diamond")
    obj = bpy.data.objects.new("Diamond", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the diamond shape
    bm = bmesh.new()

    # Create vertices for a diamond shape
    v1 = bm.verts.new((0, 0, 1))  # Top vertex
    v2 = bm.verts.new((1, 0, 0))  # Right vertex
    v3 = bm.verts.new((0, 0, -1)) # Bottom vertex
    v4 = bm.verts.new((-1, 0, 0)) # Left vertex
    
    # Create faces connecting the vertices
    bm.faces.new((v1, v2, v3))
    bm.faces.new((v1, v3, v4))
    bm.faces.new((v4, v3, v2))
    bm.faces.new((v2, v1, v4))
    
    # Finish up and write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_diamond()