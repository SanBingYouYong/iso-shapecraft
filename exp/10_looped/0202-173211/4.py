import bpy
import bmesh
from mathutils import Vector

def create_triangular_scarf(length=4, base_width=1, tip_width=0.2, thickness=0.1, bevel_amount=0.05):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("TriangularScarf")
    obj = bpy.data.objects.new("TriangularScarf", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh and define the vertices of the triangular shape
    bm = bmesh.new()
    
    # Define the vertices of the triangle with a more defined silhouette
    v1 = bm.verts.new(Vector((0, 0, 0)))            # Base left
    v2 = bm.verts.new(Vector((length, 0, 0)))       # Base right
    v3 = bm.verts.new(Vector((length / 2, base_width, 0)))  # Base peak, wider for more triangular shape
    v4 = bm.verts.new(Vector((length / 2, base_width * 0.5, 0)))  # Mid-point for folds
    v5 = bm.verts.new(Vector((length / 2, 0, 0)))    # Tip point
    
    # Create the triangle faces for the scarf
    bm.faces.new((v1, v2, v3))  # Base face
    bm.faces.new((v3, v4, v5))  # Fold face
    bm.faces.new((v4, v1, v5))   # Left fold face
    bm.faces.new((v4, v2, v5))   # Right fold face
    
    # Create the thickness by extruding the triangle
    bmesh.ops.extrude_face_region(bm, geom=[f for f in bm.faces])
    for v in bm.verts:
        v.co.z += thickness
    
    # Bevel the edges to create a softer look
    bmesh.ops.bevel(bm, geom=[v1, v2, v3, v4, v5], offset=bevel_amount, segments=8)
    
    # Finish up and write the mesh to the object
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the object mode to 'OBJECT'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add material for realism
    mat = bpy.data.materials.new(name="ScarfMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    
    # Set a more varied color palette
    bsdf.inputs['Base Color'].default_value = (0.5, 0.2, 0.8, 1)  # Example color (purple-ish)

    # Create and set a texture (ensure a valid image path)
    texture_image_path = "//path_to_your_texture_image.jpg"  # Update with a valid path
    try:
        texture_image = bpy.data.images.load(texture_image_path)
        texture = bpy.data.textures.new("FabricTexture", type='IMAGE')
        texture.image = texture_image
        
        # Add texture to the material
        tex_slot = mat.texture_slots.add()
        tex_slot.texture = texture
        tex_slot.texture_coords = 'UV'
        tex_slot.mapping = 'FLAT'
    except Exception as e:
        print(f"Could not load texture image: {e}")

    # Assign the material to the object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

create_triangular_scarf()