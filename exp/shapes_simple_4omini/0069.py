import bpy
import bmesh
from math import radians

def create_crown_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CrownMesh")
    obj = bpy.data.objects.new("Crown", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the base of the crown
    base_radius = 1.0
    height = 0.5
    num_peaks = 5
    peak_height = 0.5

    # Create the base vertices
    base_verts = []
    for i in range(num_peaks):
        angle = radians(i * (360 / num_peaks))
        x = base_radius * bpy.mathutils.cos(angle)
        y = base_radius * bpy.mathutils.sin(angle)
        base_verts.append(bmesh.verts.new((x, y, 0)))

    # Create peak vertices
    peak_verts = []
    for i in range(num_peaks):
        angle = radians(i * (360 / num_peaks))
        x = (base_radius + peak_height) * bpy.mathutils.cos(angle)
        y = (base_radius + peak_height) * bpy.mathutils.sin(angle)
        peak_verts.append(bmesh.verts.new((x, y, height)))

    # Create faces for the sides
    for i in range(num_peaks):
        v1 = base_verts[i]
        v2 = base_verts[(i + 1) % num_peaks]
        v3 = peak_verts[(i + 1) % num_peaks]
        v4 = peak_verts[i]
        bm.faces.new((v1, v2, v3, v4))

    # Create the base face
    bm.faces.new(base_verts)

    # Finish up the bmesh and write to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_crown_shape()