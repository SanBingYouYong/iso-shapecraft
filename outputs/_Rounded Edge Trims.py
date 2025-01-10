import bpy
import bmesh

def create_rounded_edge_trims(thickness=0.05, length=2.0, width=0.1, radius=0.02):
    # Create a new mesh and object for the trim
    mesh = bpy.data.meshes.new("RoundedEdgeTrim")
    obj = bpy.data.objects.new("RoundedEdgeTrim", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for the trim geometry
    bm = bmesh.new()

    # Define the vertices for the rounded edge trim
    verts = [
        bm.verts.new((-length / 2, -width / 2, 0)),
        bm.verts.new((length / 2, -width / 2, 0)),
        bm.verts.new((length / 2, width / 2, 0)),
        bm.verts.new((-length / 2, width / 2, 0)),
    ]

    # Create faces for the base rectangle
    bm.faces.new(verts)

    # Add the thickness to create the volume
    for v in verts:
        v.co.z += thickness

    # Create the top face
    bm.faces.new(verts)

    # Create rounded edges by using bevel
    bmesh.ops.bevel(bm, geom=bm.verts[:], offset=radius, segments=10)

    # Finish the mesh and update
    bm.to_mesh(mesh)
    bm.free()

    # Set the object's location and rotation if needed
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)

    # Set the shading to smooth
    for face in mesh.polygons:
        face.use_smooth = True

# Call the function to create the rounded edge trims
create_rounded_edge_trims()