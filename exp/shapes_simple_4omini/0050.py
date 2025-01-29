import bpy
import math

def create_spiral(radius, turns, height, segments):
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    bpy.ops.object.add(type='MESH', enter_editmode=True)  # Add a new mesh object
    mesh = bpy.context.object.data

    vertices = []
    edges = []
    faces = []

    for i in range(turns * segments):
        angle = i * (2 * math.pi / segments)  # Calculate angle for each segment
        x = radius * math.cos(angle) * (i / (turns * segments))  # X position
        y = radius * math.sin(angle) * (i / (turns * segments))  # Y position
        z = height * (i / (turns * segments))  # Z position
        vertices.append((x, y, z))

        if i > 0:
            edges.append((i - 1, i))  # Connect edges

    mesh.from_pydata(vertices, edges, faces)  # Create mesh from vertices and edges
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode

create_spiral(radius=1, turns=5, height=2, segments=100)