import bpy
import math

def create_wave_shape(amplitude=1, frequency=1, length=10, segments=100):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("WaveMesh")
    obj = bpy.data.objects.new("WaveObject", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices and faces
    vertices = []
    faces = []

    for i in range(segments + 1):
        x = (length / segments) * i
        y = amplitude * math.sin(frequency * (x / length) * (2 * math.pi))
        z = 0  # flat on the z-axis
        vertices.append((x, y, z))

    # Create faces between vertices
    for i in range(segments):
        faces.append((i, i + 1, i + 1, i))

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Set the object's location
    obj.location = (0, 0, 0)

create_wave_shape(amplitude=1, frequency=3, length=10, segments=100)