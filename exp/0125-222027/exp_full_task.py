import bpy
import bmesh
from mathutils import Vector

def create_hexagonal_prism(base_edge_length, height):
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create bmesh
    bm = bmesh.new()

    # Define the vertices for a hexagonal prism
    angle_offset = 360 / 6
    vertices = []
    for i in range(6):
        angle = math.radians(i * angle_offset)
        x = base_edge_length * math.cos(angle)
        y = base_edge_length * math.sin(angle)
        vertices.append(Vector((x, y, 0)))
        vertices.append(Vector((x, y, height)))

    # Create vertices in bmesh
    for v in vertices:
        bm.verts.new(v)
    
    bm.verts.ensure_lookup_table()

    # Create faces for the sides of the prism
    for i in range(6):
        v1 = bm.verts[i]
        v2 = bm.verts[(i + 1) % 6]
        v3 = bm.verts[(i + 1) % 6 + 6]
        v4 = bm.verts[i + 6]
        bm.faces.new((v1, v2, v3, v4))
    
    # Create top and bottom faces
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]))  # Bottom face
    bm.faces.new((bm.verts[6], bm.verts[7], bm.verts[5], bm.verts[4]))  # Top face

    # Finalize the bmesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function with specified dimensions
create_hexagonal_prism(base_edge_length=5, height=15)