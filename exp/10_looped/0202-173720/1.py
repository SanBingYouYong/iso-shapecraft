import bpy

def create_charging_cable(width=0.03, height=0.01, length=1.0):
    # Create a mesh and an object
    mesh = bpy.data.meshes.new("ChargingCableMesh")
    obj = bpy.data.objects.new("ChargingCable", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices for a rectangular shape with flat ends
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
    
    # Create flat ends of the cable by adjusting vertices
    end_flat_height = height * 1.5
    verts += [
        (0, 0, end_flat_height), 
        (length, 0, end_flat_height),
        (length, width, end_flat_height), 
        (0, width, end_flat_height)
    ]
    
    # Define faces for the rectangular shape and flat ends
    faces = [
        (0, 1, 2, 3), 
        (4, 5, 6, 7), 
        (8, 9, 10, 11),  # Flat end faces
        (0, 1, 5, 4), 
        (1, 2, 6, 5), 
        (2, 3, 7, 6), 
        (3, 0, 4, 7),
        (8, 9, 10, 11)  # Top flat end
    ]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Set a material for the cable to resemble a typical charging cable
    mat = bpy.data.materials.new(name="CableMaterial")
    mat.diffuse_color = (0.1, 0.1, 0.1, 1)  # A dark gray color
    obj.data.materials.append(mat)

create_charging_cable()