import bpy

def create_charging_cable(width=0.015, height=0.005, length=1.0):
    # Create a mesh and an object
    mesh = bpy.data.meshes.new("ChargingCableMesh")
    obj = bpy.data.objects.new("ChargingCable", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices for a thin rectangular shape with defined terminations
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
    
    # Create a more defined termination at both ends of the cable
    termination_length = 0.05
    end_verts = [
        (0, 0, height), 
        (length, 0, height), 
        (length, 0, height + termination_length), 
        (0, 0, height + termination_length),
        (0, width, height), 
        (length, width, height), 
        (length, width, height + termination_length), 
        (0, width, height + termination_length)
    ]
    
    verts += end_verts
    
    # Define faces for the rectangular shape and the defined terminations
    faces = [
        (0, 1, 2, 3), 
        (4, 5, 6, 7), 
        (8, 9, 10, 11),  # Termination face
        (0, 1, 5, 4), 
        (1, 2, 6, 5), 
        (2, 3, 7, 6), 
        (3, 0, 4, 7),
        (8, 9, 10, 11)  # Top termination face
    ]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Set a material for the cable to resemble a flexible charging cable
    mat = bpy.data.materials.new(name="CableMaterial")
    mat.diffuse_color = (0.2, 0.2, 0.2, 1)  # A dark gray color
    mat.specular_color = (1.0, 1.0, 1.0)  # White specular highlights for shine
    mat.roughness = 0.3  # Add some glossiness to mimic flexibility
    obj.data.materials.append(mat)

create_charging_cable()