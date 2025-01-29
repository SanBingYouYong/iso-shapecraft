import bpy
import math

def create_hexagon(radius):
    vertices = []
    edges = []
    
    # Calculate the vertices of the hexagon
    for i in range(6):
        angle = math.radians(60 * i)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y, 0))

    # Create the edges connecting the vertices
    for i in range(6):
        edges.append((i, (i + 1) % 6))

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Hexagon")
    obj = bpy.data.objects.new("Hexagon", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the vertices and edges
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

# Create a hexagon with a specified radius
create_hexagon(1)