import bpy
import math

def create_pie_slice(radius=1, angle=90, location=(0, 0, 0)):
    bpy.ops.object.select_all(action='DESELECT')
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name="PieSlice")
    obj = bpy.data.objects.new("PieSlice", mesh)
    
    # Link the object to the collection
    bpy.context.collection.objects.link(obj)
    
    # Create the geometry of the pie slice
    verts = [(0, 0, 0)]  # Center vertex
    edges = []
    faces = []

    # Calculate the number of segments based on the angle
    num_segments = 32  # More segments for a smoother curve
    segment_angle = math.radians(angle / num_segments)

    for i in range(num_segments + 1):
        theta = i * segment_angle
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        verts.append((x, y, 0))

        if i > 0:
            edges.append((0, i))  # Connect center to outer vertices
            if i < num_segments:
                faces.append((0, i, i + 1))  # Create face with center and two outer vertices

    # Create the mesh from the gathered vertices, edges, and faces
    mesh.from_pydata(verts, edges, faces)
    mesh.update()

    # Move the object to the desired location
    obj.location = location

    # Set the object as active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

create_pie_slice()