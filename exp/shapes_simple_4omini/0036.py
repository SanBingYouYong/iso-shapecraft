import bpy
import math

def create_circle_segment(radius, angle, location):
    # Create a new mesh
    mesh = bpy.data.meshes.new("CircleSegment")
    obj = bpy.data.objects.new("CircleSegment", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create the vertices for the circle segment
    vertices = []
    num_segments = 32
    angle_step = angle / num_segments
    
    # Create the points for the segment
    for i in range(num_segments + 1):
        theta = angle_step * i
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        vertices.append((x, y, 0))
    
    # Add the chord endpoints
    vertices.append((radius * math.cos(0), radius * math.sin(0), 0))  # Start point
    vertices.append((radius * math.cos(angle), radius * math.sin(angle), 0))  # End point

    # Create the faces for the segment
    faces = []
    for i in range(num_segments):
        faces.append((i, (i + 1) % (num_segments + 1), num_segments, num_segments + 1))  # Chord and arc
    
    # Create the mesh
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Move the object to the specified location
    obj.location = location

# Example usage
create_circle_segment(radius=1, angle=math.radians(90), location=(0, 0, 0))