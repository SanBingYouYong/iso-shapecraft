import bpy
import bmesh

def create_backrest_base(seat_width, seat_height):
    # Define dimensions
    backrest_width = seat_width * 1.05  # slightly wider for stability
    backrest_height = seat_height * 1.2  # taller than the seat
    backrest_thickness = 0.05  # thickness of the backrest
    rounded_radius = 0.1  # radius for rounded edges

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("BackrestBaseMesh")
    obj = bpy.data.objects.new("BackrestBase", mesh)

    # Link object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for geometry manipulation
    bm = bmesh.new()

    # Create a rectangular prism with rounded edges
    base_verts = [
        (-backrest_width / 2, -backrest_thickness / 2, 0),
        (backrest_width / 2, -backrest_thickness / 2, 0),
        (backrest_width / 2, backrest_thickness / 2, 0),
        (-backrest_width / 2, backrest_thickness / 2, 0),
        (-backrest_width / 2, -backrest_thickness / 2, backrest_height),
        (backrest_width / 2, -backrest_thickness / 2, backrest_height),
        (backrest_width / 2, backrest_thickness / 2, backrest_height),
        (-backrest_width / 2, backrest_thickness / 2, backrest_height),
    ]

    # Create faces for the rectangular prism
    base_faces = [
        (0, 1, 2, 3),  # bottom
        (4, 5, 6, 7),  # top
        (0, 1, 5, 4),  # front
        (1, 2, 6, 5),  # right
        (2, 3, 7, 6),  # back
        (3, 0, 4, 7)   # left
    ]

    for v in base_verts:
        bm.verts.new(v)

    bm.verts.ensure_lookup_table()
    
    for f in base_faces:
        bm.faces.new([bm.verts[i] for i in f])

    # Create a rounded edge effect
    bmesh.ops.bevel(bm, geom=bm.verts[:], offset=rounded_radius)

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Optionally, set the object's location
    obj.location = (0, 0, seat_height)

# Example usage
create_backrest_base(seat_width=0.5, seat_height=0.4)