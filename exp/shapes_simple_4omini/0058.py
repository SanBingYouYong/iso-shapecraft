import bpy
import bmesh
from math import radians, pi, sin, cos

def create_rounded_pentagon(radius=1, roundness=0.2):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("RoundedPentagon")
    obj = bpy.data.objects.new("RoundedPentagon", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh
    bm = bmesh.new()
    
    # Calculate the angle between vertices
    angle = 2 * pi / 5
    
    # Create pentagon vertices with rounded corners
    vertices = []
    for i in range(5):
        x = radius * cos(i * angle)
        y = radius * sin(i * angle)
        vertices.append((x, y, 0))

    # Add vertices to the bmesh
    bmesh_verts = [bm.verts.new(v) for v in vertices]
    
    # Create faces
    for i in range(5):
        v1 = bmesh_verts[i]
        v2 = bmesh_verts[(i + 1) % 5]
        v3 = bmesh_verts[(i + 1) % 5] + bmesh.Vector((roundness * cos((i + 1) * angle), roundness * sin((i + 1) * angle), 0))
        v4 = bmesh_verts[i] + bmesh.Vector((roundness * cos(i * angle), roundness * sin(i * angle), 0))
        bm.faces.new((v1, v2, v3, v4))
    
    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the object's origin to geometry
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_rounded_pentagon()