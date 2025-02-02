import bpy
import bmesh

def create_rubber_ball(radius=0.5, location=(0, 0, 0)):
    try:
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
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
        
        # Set the newly created object as active and select it
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Apply smooth shading
        bpy.ops.object.shade_smooth()
        
        # Add a subdivision surface modifier to enhance roundness
        modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        modifier.levels = 2  # Subdivision levels for viewport
        modifier.render_levels = 2  # Subdivision levels for render
        
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

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to create a rubber ball
create_rubber_ball()