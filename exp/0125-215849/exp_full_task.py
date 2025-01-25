import bpy
import bmesh

def create_hexagonal_prism(base_edge_length=5, height=15):
    # Calculate the vertices of the hexagonal base
    vertices = []
    for i in range(6):
        angle = i * (360 / 6) * (3.14159 / 180)  # Convert degrees to radians
        x = base_edge_length * bpy.mathutils.cos(angle)
        y = base_edge_length * bpy.mathutils.sin(angle)
        vertices.append((x, y, 0))  # Base vertices at z=0
        vertices.append((x, y, height))  # Top vertices at z=height

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the vertices and faces
    faces = [
        (0, 1, 3, 2), (4, 5, 7, 6),  # Side faces
        (0, 1, 5, 4), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 0, 4, 7)   # Top and bottom faces
    ]
    
    # Create mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Set shading to smooth
    bpy.ops.object.shade_smooth()

create_hexagonal_prism()