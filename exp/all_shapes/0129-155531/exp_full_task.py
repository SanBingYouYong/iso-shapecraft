import bpy
import bmesh

def create_hexagonal_prism(edge_length=5, height=15):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrismMesh")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the vertices for a hexagonal prism
    half_edge = edge_length / 2
    vertices = [
        (half_edge * 1.0, 0, 0),
        (half_edge * 0.5, half_edge * 1.732, 0),
        (-half_edge * 0.5, half_edge * 1.732, 0),
        (-half_edge * 1.0, 0, 0),
        (-half_edge * 0.5, -half_edge * 1.732, 0),
        (half_edge * 0.5, -half_edge * 1.732, 0),
        (half_edge * 1.0, 0, height),
        (half_edge * 0.5, half_edge * 1.732, height),
        (-half_edge * 0.5, half_edge * 1.732, height),
        (-half_edge * 1.0, 0, height),
        (-half_edge * 0.5, -half_edge * 1.732, height),
        (half_edge * 0.5, -half_edge * 1.732, height),
    ]

    # Create vertices in bmesh
    verts = [bm.verts.new(v) for v in vertices]

    # Create faces for the top and bottom
    bm.faces.new(verts[0:6])  # Bottom face
    bm.faces.new(verts[6:12]) # Top face

    # Create side faces
    for i in range(6):
        bm.faces.new((verts[i], verts[(i + 1) % 6], verts[(i + 1) % 6 + 6], verts[i + 6]))

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

create_hexagonal_prism()