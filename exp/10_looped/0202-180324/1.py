import bpy
import bmesh

def create_rubber_ball(radius=0.5, location=(0, 0, 0)):
    # Ensure we are in object mode
    if bpy.context.active_object is not None:
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("RubberBall")
    obj = bpy.data.objects.new("RubberBall", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh object
    bm = bmesh.new()
    
    # Create a UV sphere
    bmesh.ops.create_uv_sphere(bm, cap_tris=True, radius=radius, segments=32, ring_count=16)
    
    # Write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the location of the object
    obj.location = location
    
    # Set smooth shading
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    
    # Create a rubber-like material
    mat = bpy.data.materials.new(name="RubberMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # Dark color
    bsdf.inputs['Roughness'].default_value = 0.5  # Slightly rough
    
    # Assign the material to the object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# Call the function to create a rubber ball
create_rubber_ball()