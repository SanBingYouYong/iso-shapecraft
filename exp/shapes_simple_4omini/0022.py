import bpy

def create_parallelepiped(width, height, depth):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Parallelepiped")
    obj = bpy.data.objects.new("Parallelepiped", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices and faces of the parallelepiped
    vertices = [
        (0, 0, 0), (width, 0, 0), (width, depth, 0), (0, depth, 0),  # Bottom face
        (0, 0, height), (width, 0, height), (width, depth, height), (0, depth, height)  # Top face
    ]
    
    faces = [
        (0, 1, 2, 3),  # Bottom face
        (4, 5, 6, 7),  # Top face
        (0, 1, 5, 4),  # Front face
        (2, 3, 7, 6),  # Back face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5)   # Right face
    ]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

# Parameters for the parallelepiped
create_parallelepiped(2, 3, 1)