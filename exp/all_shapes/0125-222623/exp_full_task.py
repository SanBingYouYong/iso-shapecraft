import bpy
import bmesh

def create_cylinder_with_wall_thickness(outer_radius, wall_thickness, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CylinderWithWall")
    obj = bpy.data.objects.new("CylinderWithWall", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for the cylinder
    bm = bmesh.new()

    # Create the outer cylinder
    bmesh.ops.create_cylinder(bm, cap_tris=True, radius=outer_radius, depth=height, segments=32)

    # Create the inner cylinder
    inner_radius = outer_radius - wall_thickness
    bmesh.ops.create_cylinder(bm, cap_tris=True, radius=inner_radius, depth=height, segments=32)

    # Get the geometry and remove the inner cylinder from the outer
    bmesh.ops.delete(bm, geom=bm.verts[:] + bm.edges[:], context='FACES')

    # Finish the bmesh and assign it to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters
outer_radius = 7
wall_thickness = 1
height = 20

create_cylinder_with_wall_thickness(outer_radius, wall_thickness, height)