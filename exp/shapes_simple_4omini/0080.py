import bpy
import bmesh
import math

def create_crescent_moon(radius_outer, radius_inner, location):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CrescentMoonMesh")
    obj = bpy.data.objects.new("CrescentMoon", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh object
    bm = bmesh.new()

    # Create the outer circle
    outer_circle_verts = [bm.verts.new((radius_outer * math.cos(theta), radius_outer * math.sin(theta), 0)) for theta in [i * (math.pi / 16) for i in range(32)]]
    
    # Create the inner circle (to create the crescent shape)
    inner_circle_verts = [bm.verts.new((radius_inner * math.cos(theta), radius_inner * math.sin(theta), 0)) for theta in [i * (math.pi / 16) for i in range(32)]]

    # Connect the outer and inner vertices to form the crescent shape
    for i in range(len(outer_circle_verts)):
        v1 = outer_circle_verts[i]
        v2 = outer_circle_verts[(i + 1) % len(outer_circle_verts)]
        v3 = inner_circle_verts[(i + 1) % len(inner_circle_verts)]
        v4 = inner_circle_verts[i]

        # Create faces
        bm.faces.new((v1, v2, v3, v4))

    # Update the mesh and free the bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the location of the crescent moon
    obj.location = location

# Create a crescent moon with specified parameters
create_crescent_moon(radius_outer=1, radius_inner=0.7, location=(0, 0, 0))