import bpy
import bmesh
import math

def create_prism(base_vertices, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Prism")
    obj = bpy.data.objects.new("Prism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the geometry
    bm = bmesh.new()

    # Create the base vertices
    base_faces = []
    for i, (x, y) in enumerate(base_vertices):
        v = bm.verts.new((x, y, 0))
        base_faces.append(v)

    # Create the top vertices
    top_faces = []
    for v in base_faces:
        v_top = bm.verts.new((v.co.x, v.co.y, height))
        top_faces.append(v_top)

    # Create faces for the bottom and top bases
    bmesh.faces.new(base_faces)
    bmesh.faces.new(top_faces)

    # Create the side faces
    for i in range(len(base_faces)):
        next_i = (i + 1) % len(base_faces)
        verts = [base_faces[i], base_faces[next_i], top_faces[next_i], top_faces[i]]
        bmesh.faces.new(verts)

    # Update the mesh and free the bmesh
    bm.to_mesh(mesh)
    bm.free()

# Example parameters for a hexagonal prism
hexagon_vertices = [(math.cos(math.radians(angle)), math.sin(math.radians(angle)), 0) for angle in range(0, 360, 60)]
create_prism(hexagon_vertices, 2)