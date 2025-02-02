import bpy

def create_bread_box():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the base of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
    base = bpy.context.object
    base.name = "BreadBox_Base"
    base.scale[0] = 1.5  # Length
    base.scale[1] = 1    # Width
    base.scale[2] = 0.6  # Height
    bpy.ops.object.shade_smooth()  # Smooth shading for realism

    # Add bevel to edges for a more realistic look
    bpy.ops.object.modifier_add(type='BEVEL')
    base.modifiers["Bevel"].width = 0.05
    base.modifiers["Bevel"].segments = 5
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # Create the lid of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.2))
    lid = bpy.context.object
    lid.name = "BreadBox_Lid"
    lid.scale[0] = 1.4  # Slightly smaller than base for snug fit
    lid.scale[1] = 0.9  # Slightly smaller than base for snug fit
    lid.scale[2] = 0.25  # Height (thinner than the base)
    bpy.ops.object.shade_smooth()  # Smooth shading for realism

    # Add bevel to edges of the lid for realism
    bpy.ops.object.modifier_add(type='BEVEL')
    lid.modifiers["Bevel"].width = 0.05
    lid.modifiers["Bevel"].segments = 5
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # Create a hinge detail on the side of the lid
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(1.4, 0, 1.2))
    hinge_detail = bpy.context.object
    hinge_detail.name = "Hinge_Detail"
    hinge_detail.scale[0] = 0.1  # Width of the hinge
    hinge_detail.scale[1] = 0.1  # Depth
    hinge_detail.scale[2] = 0.1  # Height
    bpy.ops.object.shade_smooth()  # Smooth shading for realism

    # Create a prominent handle for the lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.4, location=(0, 1.1, 1.4))
    handle = bpy.context.object
    handle.name = "BreadBox_Handle"
    handle.rotation_euler[0] = 1.5708  # Rotate to align horizontally
    bpy.ops.object.shade_smooth()  # Smooth shading for realism

    # Add bevel to the handle for more definition
    bpy.ops.object.modifier_add(type='BEVEL')
    handle.modifiers["Bevel"].width = 0.02
    handle.modifiers["Bevel"].segments = 5
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # Create a hinge cylinder for visual representation
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.4, location=(1.4, 0, 1.2))
    hinge = bpy.context.object
    hinge.name = "BreadBox_Hinge"
    hinge.rotation_euler[0] = 1.5708  # Rotate to align with the lid
    hinge.location.z += 0.1  # Raise hinge slightly for visibility
    bpy.ops.object.shade_smooth()  # Smooth shading for realism

    # Add bevel to hinge for more definition
    bpy.ops.object.modifier_add(type='BEVEL')
    hinge.modifiers["Bevel"].width = 0.01
    hinge.modifiers["Bevel"].segments = 5
    bpy.ops.object.modifier_apply(modifier="Bevel")

create_bread_box()