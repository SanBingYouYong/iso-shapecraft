import bpy
import math

def create_semicircular_arc(radius, segments):
    # Create a new mesh
    mesh = bpy.data.meshes.new("SemicircularArc")
    obj = bpy.data.objects.new("SemicircularArc", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create vertices
    verts = []
    for i in range(segments + 1):
        angle = math.pi * (i / segments)  # Angle from 0 to pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        verts.append((x, y, 0))

    # Create edges for the arc, connecting the vertices
    edges = [(i, i + 1) for i in range(segments)]

    # Create the mesh from the vertices and edges
    mesh.from_pydata(verts, edges, [])
    mesh.update()

create_semicircular_arc(radius=1, segments=32)