import bpy
import bmesh
import math

def create_heart_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HeartMesh")
    obj = bpy.data.objects.new("Heart", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the bmesh for the heart shape
    bm = bmesh.new()
    
    # Define heart shape parameters
    scale = 1.0
    segments = 32
    height = 1.5

    # Create vertices for the heart shape
    for i in range(segments + 1):
        theta = i * (math.pi / 2) / segments
        x = (scale * 16 * math.sin(theta) ** 3) / 16
        y = (scale * (13 * math.cos(theta) - 5 * math.cos(2 * theta) - 2 * math.cos(3 * theta) - math.cos(4 * theta))) / 16
        z = -height * (1 - (i / segments))  # Create a pointed bottom

        bmesh.ops.create_vert(bm, co=(x, y, z))

    # Create faces
    verts = [v for v in bm.verts]
    for i in range(segments):
        v1 = verts[i]
        v2 = verts[i + 1]
        v3 = verts[0]  # Connect to the first vertex for the base face
        bmesh.ops.create_face(bm, verts=[v1, v2, v3])

    # Finish the bmesh and write to mesh
    bm.to_mesh(mesh)
    bm.free()

create_heart_shape()