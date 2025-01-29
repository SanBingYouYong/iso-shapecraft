import bpy

def create_pyramid():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Define the vertices and faces for the pyramid
    vertices = [
        (1, 1, 0),   # Base vertex 1
        (1, -1, 0),  # Base vertex 2
        (-1, -1, 0), # Base vertex 3
        (-1, 1, 0),  # Base vertex 4
        (0, 0, 1)    # Apex vertex
    ]
    
    faces = [
        (0, 1, 4),  # Triangle face 1
        (1, 2, 4),  # Triangle face 2
        (2, 3, 4),  # Triangle face 3
        (3, 0, 4),  # Triangle face 4
        (0, 1, 2, 3) # Square base
    ]
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Pyramid")
    obj = bpy.data.objects.new("Pyramid", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

create_pyramid()