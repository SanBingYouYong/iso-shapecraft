import bpy
import math

def create_v_shape(angle_degrees, length):
    # Calculate the coordinates for the V shape
    angle_radians = math.radians(angle_degrees)
    half_length = length / 2

    # Create vertices for the V shape
    verts = [
        (0, 0, 0),  # Vertex 0
        (half_length * math.cos(angle_radians / 2), half_length * math.sin(angle_radians / 2), 0),  # Vertex 1
        (-half_length * math.cos(angle_radians / 2), half_length * math.sin(angle_radians / 2), 0)  # Vertex 2
    ]
    
    # Create edges for the V shape
    edges = [(0, 1), (0, 2)]

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("VShapeMesh")
    obj = bpy.data.objects.new("VShape", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the mesh from the vertices and edges
    mesh.from_pydata(verts, edges, [])
    mesh.update()

# Create a V-shaped line with an open angle of 60 degrees and length of 2 units
create_v_shape(60, 2)