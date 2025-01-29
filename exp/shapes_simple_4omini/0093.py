import bpy
import math

def create_spiral(radius, height, turns, segments):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("SpiralMesh")
    obj = bpy.data.objects.new("Spiral", mesh)

    # Link object to the scene
    bpy.context.collection.objects.link(obj)

    # Create vertices and faces
    vertices = []
    edges = []
    faces = []

    for t in range(turns * segments + 1):
        angle = t * (2 * math.pi / segments)  # Angle for each segment
        r = radius * (1 - t / (turns * segments))  # Decrease radius for tight loops
        z = height * (t / (turns * segments))  # Linear height increase

        x = r * math.cos(angle)
        y = r * math.sin(angle)

        vertices.append((x, y, z))

        if t > 0:
            edges.append((t - 1, t))

    # Create mesh from vertices and edges
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

# Parameters for the spiral
create_spiral(radius=1, height=5, turns=5, segments=100)