import bpy
import math

def create_parallelogram(length, width, height):
    # Define vertices for a parallelogram
    vertices = [
        (0, 0, 0),  # Vertex 0
        (length, 0, 0),  # Vertex 1
        (length - width * math.cos(math.radians(30)), width * math.sin(math.radians(30)), 0),  # Vertex 2
        (-width * math.cos(math.radians(30)), width * math.sin(math.radians(30)), 0),  # Vertex 3
        (0, 0, height),  # Vertex 4
        (length, 0, height),  # Vertex 5
        (length - width * math.cos(math.radians(30)), width * math.sin(math.radians(30)), height),  # Vertex 6
        (-width * math.cos(math.radians(30)), width * math.sin(math.radians(30)), height)  # Vertex 7
    ]

    # Define edges (not needed for a mesh but included for clarity)
    edges = []

    # Define faces
    faces = [
        (0, 1, 2, 3),  # Bottom face
        (4, 5, 6, 7),  # Top face
        (0, 1, 5, 4),  # Side face 1
        (1, 2, 6, 5),  # Side face 2
        (2, 3, 7, 6),  # Side face 3
        (3, 0, 4, 7)   # Side face 4
    ]

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Parallelogram")
    obj = bpy.data.objects.new("Parallelogram", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the vertices, edges, and faces
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

# Create a parallelogram with specified dimensions
create_parallelogram(length=2, width=1, height=1)