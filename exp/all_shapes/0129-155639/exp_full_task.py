import bpy
import math

def create_undulating_plane(width, height, amplitude, wavelength, subdivisions):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("UndulatingPlane")
    obj = bpy.data.objects.new("UndulatingPlane", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create vertices
    vertices = []
    faces = []
    
    # Generate the vertices
    for x in range(subdivisions):
        for y in range(subdivisions):
            x_pos = (x / (subdivisions - 1)) * width - (width / 2)
            y_pos = (y / (subdivisions - 1)) * height - (height / 2)
            z_pos = amplitude * math.sin((x_pos / wavelength) * (2 * math.pi))
            vertices.append((x_pos, y_pos, z_pos))
    
    # Create faces
    for x in range(subdivisions - 1):
        for y in range(subdivisions - 1):
            v1 = x * subdivisions + y
            v2 = v1 + 1
            v3 = v1 + subdivisions
            v4 = v3 + 1
            faces.append((v1, v2, v4, v3))
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

# Parameters: width, height, amplitude, wavelength, subdivisions
create_undulating_plane(20, 15, 2, 5, 30)