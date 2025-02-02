import bpy

def create_red_sphere():
    # Delete all existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a UV Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    
    # Get the created sphere object
    sphere = bpy.context.active_object
    
    # Create a new material
    material = bpy.data.materials.new(name="RedMaterial")
    material.diffuse_color = (1, 0, 0, 1)  # RGBA for red color
    
    # Assign the material to the sphere
    if sphere.data.materials:
        sphere.data.materials[0] = material
    else:
        sphere.data.materials.append(material)

create_red_sphere()