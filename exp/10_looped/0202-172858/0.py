import bpy

def create_bread_box():
    # Create the base of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    base = bpy.context.object
    base.name = "BreadBox_Base"
    base.scale[0] = 1.5  # Length
    base.scale[1] = 1    # Width
    base.scale[2] = 0.5  # Height

    # Create the lid of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 2))
    lid = bpy.context.object
    lid.name = "BreadBox_Lid"
    lid.scale[0] = 1.5  # Length
    lid.scale[1] = 1    # Width
    lid.scale[2] = 0.2  # Height (thinner than the base)

    # Move the lid to the correct position
    lid.location.z += 0.25  # Adjusting position for the hinge effect

    # Create a hinge for the lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.5, location=(1.5, 0, 2))
    hinge = bpy.context.object
    hinge.name = "BreadBox_Hinge"
    hinge.rotation_euler[0] = 1.5708  # Rotate to align with the lid

create_bread_box()