import bpy

def create_charging_cable(width=0.008, height=0.003, length=1.0):
    # Create a mesh and an object
    mesh = bpy.data.meshes.new("ChargingCableMesh")
    obj = bpy.data.objects.new("ChargingCable", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices for a thin rectangular shape with square ends
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
    
    # Define square terminations for the cable ends
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
    
    # Define faces for the rectangular shape and square terminations
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

    # Create a realistic material for the cable
    mat = bpy.data.materials.new(name="CableMaterial")
    mat.use_nodes = True  # Enable nodes for better material control
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # Dark gray
    bsdf.inputs['Roughness'].default_value = 0.3  # Slightly glossy
    bsdf.inputs['Specular'].default_value = 0.5  # Reflectivity

    # Apply the material to the object
    obj.data.materials.append(mat)

create_charging_cable()