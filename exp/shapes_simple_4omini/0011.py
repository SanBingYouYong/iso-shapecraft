import bpy
import bmesh
from math import radians

def create_star(size=1, depth=0.1):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Star")
    obj = bpy.data.objects.new("Star", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the star shape
    bm = bmesh.new()

    # Define the star points
    points = [
        (0, size, 0),
        (size * 0.2245, size * 0.309, 0),
        (size, size * 0.309, 0),
        (size * 0.3632, size * 0.118, 0),
        (size * 0.4472, -size * 0.309, 0),
        (0, -size * 0.118, 0),
        (-size * 0.4472, -size * 0.309, 0),
        (-size * 0.3632, size * 0.118, 0),
        (-size, size * 0.309, 0),
        (-size * 0.2245, size * 0.309, 0)
    ]

    # Create vertices
    verts = [bm.verts.new(point) for point in points]

    # Create faces for the star
    faces = [
        (verts[0], verts[1], verts[2], verts[3], verts[4]),
        (verts[0], verts[4], verts[5], verts[6], verts[7]),
        (verts[0], verts[7], verts[8], verts[9], verts[1]),
    ]
    
    for face in faces:
        bm.faces.new(face)

    # Finish up, write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the object to be selectable and active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

# Call the function to create the star
create_star(size=1, depth=0.1)