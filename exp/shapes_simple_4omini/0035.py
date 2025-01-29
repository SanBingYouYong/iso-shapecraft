import bpy
import math

def create_circle_sector(radius, angle, location=(0, 0, 0)):
    # Clear the existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CircleSector")
    obj = bpy.data.objects.new("CircleSector", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Generate vertices and faces for the sector
    vertices = [(0, 0, 0)]  # Center point
    num_segments = 32  # Number of segments for the arc
    angle_step = angle / num_segments
    
    for i in range(num_segments + 1):
        theta = math.radians(i * angle_step)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        vertices.append((x, y, 0))
    
    # Create faces
    faces = [(0, i + 1, i + 2) for i in range(num_segments)]
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    
    # Move the object to the specified location
    obj.location = location

create_circle_sector(radius=2, angle=90, location=(0, 0, 0))