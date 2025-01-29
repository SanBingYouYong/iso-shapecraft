import bpy
import bmesh
import math

def create_rounded_star(radius_outer, radius_inner, thickness, num_points):
    bpy.ops.object.select_all(action='DESELECT')
    
    # Create a new mesh
    mesh = bpy.data.meshes.new("RoundedStar")
    obj = bpy.data.objects.new("RoundedStar", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create the star shape
    angle_step = math.pi / num_points
    for i in range(num_points * 2):
        angle = i * angle_step
        r = radius_outer if i % 2 == 0 else radius_inner
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        bmesh.ops.create_circle(bm, cap_tris=True, radius=r, location=(x, y, 0), segments=8)

    # Create faces
    verts = [v for v in bm.verts]
    for i in range(len(verts)):
        v1 = verts[i]
        v2 = verts[(i + 1) % len(verts)]
        v3 = verts[(i + 1 + num_points) % len(verts)]
        v4 = verts[(i + num_points) % len(verts)]
        bmesh.ops.face_create(bm, verts=[v1, v2, v3, v4])

    # Extrude to give thickness
    for v in bm.verts:
        v.co.z += thickness
    
    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the rounded star
radius_outer = 1.0
radius_inner = 0.5
thickness = 0.2
num_points = 5

create_rounded_star(radius_outer, radius_inner, thickness, num_points)