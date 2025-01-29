import bpy
import bmesh
from math import radians

def create_octagon(size):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Octagon")
    obj = bpy.data.objects.new("Octagon", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the octagon geometry
    bm = bmesh.new()
    
    # Calculate the angle for each vertex
    angle = 360 / 8
    vertices = []

    for i in range(8):
        x = size * cos(radians(i * angle))
        y = size * sin(radians(i * angle))
        vertices.append(bm.verts.new((x, y, 0)))

    # Create the faces of the octagon
    bm.faces.new(vertices)

    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function with the desired size of the octagon
create_octagon(1)