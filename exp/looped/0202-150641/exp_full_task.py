import bpy

def create_red_sphere():
    # Create a new mesh and object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    sphere = bpy.context.object
    
    # Set the material
    material = bpy.data.materials.new(name="Red Material")
    material.diffuse_color = (1, 0, 0, 1)  # RGBA for red color
    sphere.data.materials.append(material)

create_red_sphere()