import bpy
import bmesh
from math import radians

def create_hexagonal_prism(base_edge_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the bmesh object
    bm = bmesh.new()

    # Create the hexagonal base
    vertices = []
    for i in range(6):
        angle = radians(60 * i)
        x = base_edge_length * 0.5 * (1 if i % 2 == 0 else 0)
        y = base_edge_length * 0.5 * (1 if i % 2 == 1 else 0)
        z = 0
        vertices.append(bm.verts.new((x * (1 if i % 2 == 0 else -1), y * (1 if i % 2 == 1 else -1), z)))

    # Create the top and bottom hexagonal faces
    bottom_face = bm.faces.new(vertices[:])
    top_face = bm.faces.new([bm.verts.new((v.co.x, v.co.y, height)) for v in vertices])

    # Connect the top and bottom faces
    for i in range(6):
        bm.edges.new((vertices[i], top_face.verts[i]))

    # Finish the bmesh
    bm.to_mesh(mesh)
    bm.free()

create_hexagonal_prism(5, 15)