import bpy

def create_red_sphere():
    # Delete default cube if it exists
    if "Cube" in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()

    # Create a sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    sphere = bpy.context.object

    # Set the material
    material = bpy.data.materials.new(name="RedMaterial")
    material.diffuse_color = (1, 0, 0, 1)  # Red color in RGBA
    sphere.data.materials.append(material)

create_red_sphere()