import bpy
import bmesh
import math

def create_rounded_diamond_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("RoundedDiamond")
    obj = bpy.data.objects.new("RoundedDiamond", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()
    
    # Define parameters for the rounded diamond shape
    radius = 1.0
    height = 2.0
    segments = 16

    # Create the base shape
    for i in range(segments):
        angle = math.radians(i * (360 / segments))
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)

        # Create the top and bottom vertices
        bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, location=(x, y, height / 2), segments=segments)
        bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, location=(x, y, -height / 2), segments=segments)

    # Create the diamond shape by connecting the vertices
    for i in range(segments):
        v1 = bm.verts[i]
        v2 = bm.verts[(i + 1) % segments]
        v3 = bm.verts[i + segments]
        v4 = bm.verts[(i + 1) % segments + segments]

        # Create faces for the sides
        bmesh.ops.create_face(bm, verts=[v1, v2, v4, v3])

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the object's origin to the geometry's center
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_rounded_diamond_shape()