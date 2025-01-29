import bpy

def create_rectangle(length, width):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("RectangleMesh")
    obj = bpy.data.objects.new("Rectangle", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Define the vertices and faces of the rectangle
    verts = [
        (0, 0, 0),  # Bottom left
        (length, 0, 0),  # Bottom right
        (length, width, 0),  # Top right
        (0, width, 0)  # Top left
    ]
    
    faces = [(0, 1, 2, 3)]  # One face for the rectangle
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

# Call the function with desired dimensions
create_rectangle(2, 1)