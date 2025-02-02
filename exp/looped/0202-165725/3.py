import bpy
import bmesh

def create_refined_tapered_wedge(length=2.0, base_width=0.5, height=1.0, taper_amount=0.2, subdivisions=5):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("RefinedTaperedWedge")
    obj = bpy.data.objects.new("RefinedTaperedWedge", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh data
    bm = bmesh.new()

    # Define vertices for a tapered wedge shape with adjusted dimensions
    v1 = bm.verts.new((0, 0, 0))  # Base back left
    v2 = bm.verts.new((length, 0, 0))  # Base back right
    v3 = bm.verts.new((length, base_width, 0))  # Base front right
    v4 = bm.verts.new((0, base_width, 0))  # Base front left

    # Add more subdivided vertices to enhance smoothness on the tapered end
    for i in range(subdivisions + 1):
        t = i / subdivisions
        # Gradually taper the vertices towards a sharper end
        bm.verts.new((length * (1 - t * taper_amount), 0, height * t))  # Back edge
        bm.verts.new((length * (1 - t * taper_amount), base_width, height * t))  # Front edge
    
    # Collect all the new vertices for easier access
    new_verts = list(bm.verts)[4:]  # Skip the first four base vertices

    # Create faces for the tapered wedge
    bm.faces.new((v1, v2, new_verts[0], new_verts[1]))  # Back face
    bm.faces.new((v2, v3, new_verts[-1], new_verts[-2]))  # Right face
    bm.faces.new((v3, v4, new_verts[3], new_verts[2]))  # Front face
    bm.faces.new((v4, v1, new_verts[1], new_verts[0]))  # Left face
    
    # Side faces connecting to the top
    for i in range(1, len(new_verts) - 1):
        bm.faces.new((new_verts[i - 1], new_verts[i], new_verts[i + 1], new_verts[i + len(new_verts) // 2]))

    # Finish the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Smooth the shading
    for face in mesh.polygons:
        face.use_smooth = True

    # Apply a subdivision surface modifier for smoother appearance
    modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    modifier.levels = 2
    modifier.render_levels = 2

    # Set the origin to the center of the geometry
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_refined_tapered_wedge()