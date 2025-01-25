import bpy

def create_red_sphere(radius=1, location=(0, 0, 0)):
    # Create a new sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    
    # Get the newly created sphere
    sphere = bpy.context.object
    
    # Create a new material
    material = bpy.data.materials.new(name="RedMaterial")
    material.diffuse_color = (1, 0, 0, 1)  # RGBA for red
    
    # Assign the material to the sphere
    if sphere.data.materials:
        sphere.data.materials[0] = material
    else:
        sphere.data.materials.append(material)

create_red_sphere()