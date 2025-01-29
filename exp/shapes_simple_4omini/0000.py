import bpy

def create_square(size):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("SquareMesh")
    obj = bpy.data.objects.new("Square", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the square vertices and faces
    vertices = [
        (size / 2, size / 2, 0),  # Top Right
        (size / 2, -size / 2, 0), # Bottom Right
        (-size / 2, -size / 2, 0),# Bottom Left
        (-size / 2, size / 2, 0)  # Top Left
    ]
    
    faces = [(0, 1, 2, 3)]  # One face made of all four vertices

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

create_square(2)