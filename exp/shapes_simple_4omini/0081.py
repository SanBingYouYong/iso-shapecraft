import bpy
import bmesh
import math
import random

def create_squiggly_line(num_points=10, amplitude=0.5, frequency=1.0):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("SquigglyLine")
    obj = bpy.data.objects.new("SquigglyLineObject", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh object to build the geometry
    bm = bmesh.new()
    
    # Generate random points for the squiggly line
    for i in range(num_points):
        x = i * 0.5  # Spacing between points
        y = amplitude * math.sin(frequency * x + random.uniform(-math.pi/4, math.pi/4))  # Y position with irregularity
        z = random.uniform(-0.2, 0.2)  # Random Z position for irregularity
        bmesh.ops.create_vert(bm, co=(x, y, z))

    # Create edges between the points
    verts = list(bm.verts)
    for i in range(len(verts) - 1):
        bmesh.ops.create_edge(bm, v1=verts[i], v2=verts[i + 1])

    # Finish up and write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_squiggly_line()