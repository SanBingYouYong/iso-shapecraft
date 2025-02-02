import bpy

def create_charging_cable(width=0.02, height=0.01, length=1.0):
    # Create a mesh and an object
    mesh = bpy.data.meshes.new("ChargingCableMesh")
    obj = bpy.data.objects.new("ChargingCable", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices and faces for the rectangular shape
    verts = [
        (0, 0, 0), 
        (length, 0, 0), 
        (length, width, 0), 
        (0, width, 0), 
        (0, 0, height), 
        (length, 0, height), 
        (length, width, height), 
        (0, width, height)
    ]
    
    faces = [
        (0, 1, 2, 3), 
        (4, 5, 6, 7), 
        (0, 1, 5, 4), 
        (1, 2, 6, 5), 
        (2, 3, 7, 6), 
        (3, 0, 4, 7)
    ]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

create_charging_cable()