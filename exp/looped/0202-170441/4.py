import bpy
import bmesh
import math

def create_wedge(length, width, height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Wedge")
    obj = bpy.data.objects.new("Wedge", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the shape
    bm = bmesh.new()

    # Define the vertices for the base of the wedge
    v1 = bm.verts.new((0, 0, 0))  # Bottom left
    v2 = bm.verts.new((length, 0, 0))  # Bottom right
    v3 = bm.verts.new((length, width, 0))  # Top right
    v4 = bm.verts.new((0, width, 0))  # Top left

    # Define the smooth tapered end
    taper_height = height * 1.5  # Increased height for a more pronounced taper
    num_taper_vertices = 16  # More vertices for a smoother transition
    for i in range(num_taper_vertices):
        angle = (math.pi / (num_taper_vertices - 1)) * i  # Distribute vertices in a circular manner
        radius = 0.3 * (1 - (i / (num_taper_vertices - 1)))  # Decrease radius for smooth taper
        x = (length * 0.5) + (radius * math.cos(angle))
        y = (width * 0.5) + (radius * math.sin(angle))
        z = taper_height
        bm.verts.new((x, y, z))

    # Create faces for the bottom
    bm.faces.new((v1, v2, v3, v4))  # Bottom face

    # Create side faces with smoother transitions
    taper_verts = list(bm.verts)[4:]  # Get the newly created taper vertices
    for i in range(len(taper_verts)):
        v_start = taper_verts[i]
        v_end = taper_verts[(i + 1) % len(taper_verts)]  # Wrap around
        # Create side faces for a smoother taper
        if i < len(taper_verts) - 1:
            bm.faces.new((v1, v2, v_start))
            bm.faces.new((v2, v3, v_end))
            bm.faces.new((v3, v4, v_start))
            bm.faces.new((v4, v1, v_end))

    # Finish up and write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Recalculate normals for smooth shading
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

create_wedge(2, 1, 0.5)