import bpy

def create_shoe_box(length, width, height, bevel_depth):
    bpy.ops.mesh.primitive_cube_add(size=1)
    shoe_box = bpy.context.object
    shoe_box.scale = (length / 2, width / 2, height / 2)
    shoe_box.location = (0, 0, height / 2)
    
    # Add a bevel modifier for rounded edges
    bevel_modifier = shoe_box.modifiers.new(name="Bevel", type='BEVEL')
    bevel_modifier.width = bevel_depth
    bevel_modifier.segments = 10
    bevel_modifier.profile = 0.5  # Adjust for a rounded edge effect

create_shoe_box(4, 1, 0.3, 0.05)