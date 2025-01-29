import bpy
import math

def create_flower_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("FlowerMesh")
    flower_object = bpy.data.objects.new("Flower", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(flower_object)
    
    # Create geometry
    vertices = []
    faces = []
    
    # Parameters for the flower
    petal_count = 5
    petal_radius = 1.0
    petal_height = 0.5
    petal_angle = 2 * math.pi / petal_count
    
    # Create vertices for the petals
    for i in range(petal_count):
        angle = i * petal_angle
        x = petal_radius * math.cos(angle)
        y = petal_radius * math.sin(angle)
        
        # Add petal vertices
        vertices.append((x, y, 0))
        vertices.append((x * 0.5, y * 0.5, petal_height))  # Top of the petal
        
        # Create faces between the vertices
        if i > 0:
            faces.append((2 * (i - 1), 2 * (i - 1) + 1, 2 * i + 1, 2 * i))
    
    # Closing the last petal face
    faces.append((2 * (petal_count - 1), 2 * (petal_count - 1) + 1, 1, 0))
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

create_flower_shape()