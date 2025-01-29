import bpy
import math

def create_parallelogram(length, width, angle):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Parallelogram")
    obj = bpy.data.objects.new("Parallelogram", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices of the parallelogram
    angle_rad = math.radians(angle)
    vertices = [
        (0, 0, 0),  # Bottom-left
        (length, 0, 0),  # Bottom-right
        (length - width * math.cos(angle_rad), width * math.sin(angle_rad), 0),  # Top-right
        (-width * math.cos(angle_rad), width * math.sin(angle_rad), 0)  # Top-left
    ]

    # Define the faces
    faces = [(0, 1, 2, 3)]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

# Parameters: length, width, angle (in degrees)
create_parallelogram(2, 1, 60)