import bpy
import math

def create_logarithmic_spiral(turns=5, points_per_turn=100, radius_factor=0.1, height_increment=0.1):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("LogarithmicSpiral")
    obj = bpy.data.objects.new("LogarithmicSpiral", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Define vertices and faces
    vertices = []
    edges = []
    
    for i in range(turns * points_per_turn):
        angle = i * (math.pi * 2 / points_per_turn)  # angle for each point
        radius = radius_factor * math.exp(0.2 * angle)  # logarithmic radius
        height = height_increment * i / points_per_turn  # incremental height
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = height
        
        vertices.append((x, y, z))
        
        if i > 0:
            edges.append((i - 1, i))  # create edges between consecutive points

    # Create mesh from vertices and edges
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

create_logarithmic_spiral()