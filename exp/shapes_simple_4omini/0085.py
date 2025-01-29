import bpy
import bmesh
from math import radians

def create_flame_shape():
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("FlameMesh")
    obj = bpy.data.objects.new("Flame", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the flame geometry
    bm = bmesh.new()

    # Define flame parameters
    flame_height = 2.0
    flame_width = 0.5
    flame_tip = flame_height * 0.8

    # Create the base of the flame
    base_verts = [
        (-flame_width, 0, 0),
        (flame_width, 0, 0),
        (0, 0, flame_height)
    ]
    
    # Create the curve of the flame body
    curve_verts = [
        (-flame_width * 0.5, 0, flame_tip),
        (0, 0, flame_height * 0.6),
        (flame_width * 0.5, 0, flame_tip)
    ]

    # Add base vertices
    for v in base_verts:
        bm.verts.new(v)

    # Add curve vertices
    for v in curve_verts:
        bm.verts.new(v)

    # Create faces for the flame shape
    bm.verts.ensure_lookup_table()
    bmesh.ops.context_create(bm)
    bmesh.ops.context_add_face(bm, [bm.verts[0], bm.verts[1], bm.verts[2]])
    bmesh.ops.context_add_face(bm, [bm.verts[0], bm.verts[2], bm.verts[3]])
    bmesh.ops.context_add_face(bm, [bm.verts[1], bm.verts[2], bm.verts[4]])
    bmesh.ops.context_add_face(bm, [bm.verts[3], bm.verts[4], bm.verts[2]])

    # Update the mesh with the bmesh data
    bm.to_mesh(mesh)
    bm.free()

create_flame_shape()