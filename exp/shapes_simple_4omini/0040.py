import bpy
import math

def create_zigzag_line(length=5, segments=10, height=1):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name="ZigzagLine")
    obj = bpy.data.objects.new("ZigzagLine", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Define vertices and edges for the zigzag line
    vertices = []
    edges = []

    for i in range(segments + 1):
        x = (length / segments) * i
        y = height * (-1) ** i  # Alternate between -height and height
        vertices.append((x, y, 0))
        if i > 0:
            edges.append((i - 1, i))

    # Create the mesh from the vertices and edges
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

create_zigzag_line()