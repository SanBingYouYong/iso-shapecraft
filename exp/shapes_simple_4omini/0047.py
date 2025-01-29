import bpy
import math

def create_circular_sector(radius, angle, location):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CircularSector")
    obj = bpy.data.objects.new("CircularSector", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create vertices for the circular sector
    vertices = []
    vertices.append((0, 0, 0))  # Center vertex
    segments = 32  # Number of segments for the arc
    for i in range(segments + 1):
        theta = (angle / segments) * i
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        vertices.append((x, y, 0))

    # Create faces for the circular sector
    faces = []
    for i in range(1, segments + 1):
        faces.append((0, i, i + 1 if i + 1 <= segments else 1))

    # Create the mesh from vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Set the location of the object
    obj.location = location

# Parameters for the circular sector
radius = 1.0
angle = math.radians(90)  # 90 degrees in radians
location = (0, 0, 0)

create_circular_sector(radius, angle, location)