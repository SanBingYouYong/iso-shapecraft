import bpy
import bmesh
from math import radians

def create_teardrop():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Teardrop")
    obj = bpy.data.objects.new("Teardrop", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a BMesh to define the geometry
    bm = bmesh.new()
    
    # Define vertices of a teardrop shape
    verts = [
        (0, 0, 0),  # Bottom point
        (1, 0, 1),  # Right side
        (0, 1, 1),  # Top point
        (-1, 0, 1), # Left side
    ]
    
    # Create the vertices
    vlist = [bm.verts.new(v) for v in verts]
    
    # Define faces based on vertices
    faces = [
        (vlist[0], vlist[1], vlist[2]),
        (vlist[0], vlist[2], vlist[3]),
        (vlist[0], vlist[1], vlist[3]),
        (vlist[1], vlist[2], vlist[3]),
    ]
    
    for f in faces:
        bm.faces.new(f)
    
    # Update the mesh with the new geometry
    bm.to_mesh(mesh)
    bm.free()

    # Move the object to the center
    obj.location = (0, 0, 0)

create_teardrop()