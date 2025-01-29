import bpy
import bmesh
from math import radians

def create_stylized_leaf():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("StylizedLeaf")
    obj = bpy.data.objects.new("StylizedLeaf", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the leaf shape
    bm = bmesh.new()

    # Define the vertices of the leaf
    verts = [
        bm.verts.new((0, 0, 0)),  # Base point
        bm.verts.new((0.5, 0, 0)),  # Right tip
        bm.verts.new((0.25, 0.5, 0)),  # Top tip
        bm.verts.new((-0.25, 0.5, 0)),  # Left tip
        bm.verts.new((-0.5, 0, 0)),  # Left base
    ]

    # Create faces to form the leaf shape
    bm.faces.new((verts[0], verts[1], verts[2]))
    bm.faces.new((verts[0], verts[2], verts[3]))
    bm.faces.new((verts[0], verts[3], verts[4]))
    
    # Optionally add some thickness
    for v in verts:
        v.co.z += 0.1  # Raise z to give thickness

    # Create the mesh from the bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the object's origin to geometry center
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_stylized_leaf()