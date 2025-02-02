import bpy

def create_bread_box():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the base of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
    base = bpy.context.object
    base.scale[0] = 0.8  # Width
    base.scale[1] = 0.4  # Depth
    base.scale[2] = 0.5  # Height

    # Create the lid of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.3))
    lid = bpy.context.object
    lid.scale[0] = 0.8  # Width
    lid.scale[1] = 0.4  # Depth
    lid.scale[2] = 0.1  # Height

    # Create a hinge for the lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.1, location=(0, -0.4, 1.3))
    hinge = bpy.context.object
    hinge.rotation_euler[0] = 1.5708  # Rotate to align with the lid

    # Parent the lid to the hinge
    lid.parent = hinge

# Run the function to create the bread box
create_bread_box()