import bpy
import math

def create_star_prism(points=8, radius=6, height=10):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("StarPrismMesh")
    obj = bpy.data.objects.new("StarPrism", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create vertices and faces for the star-shaped base
    vertices = []
    faces = []
    
    for i in range(points):
        angle = i * (2 * math.pi / points)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y, 0))  # Base vertices
        vertices.append((x * 0.5, y * 0.5, height))  # Top vertices

    # Create the faces for the base and sides
    for i in range(points):
        next_i = (i + 1) % points
        # Base face
        faces.append((i * 2, next_i * 2, next_i * 2 + 1, i * 2 + 1))
        # Side faces
        faces.append((i * 2, i * 2 + 1, next_i * 2 + 1, next_i * 2))

    # Create the mesh
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

# Call the function to create the star prism
create_star_prism()