import bpy

def create_rounded_rectangle_box(width, height, depth, radius):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Scale to desired dimensions
    bpy.ops.transform.resize(value=(width / 2, depth / 2, height / 2))
    
    # Add a subdivision surface modifier for smoothness
    bpy.ops.object.modifier_add(type='SUBSURF')
    obj.modifiers['Subdivision'].levels = 2
    bpy.ops.object.shade_smooth()
    
    # Apply the modifier to keep the geometry
    bpy.ops.object.modifier_apply(modifier='Subdivision')
    
    # Add the bevel modifier to round the edges
    bpy.ops.object.modifier_add(type='BEVEL')
    obj.modifiers['Bevel'].width = radius
    obj.modifiers['Bevel'].segments = 10
    bpy.ops.object.modifier_apply(modifier='Bevel')
    
    bpy.ops.object.mode_set(mode='OBJECT')

# Parameters: width, height, depth, radius
create_rounded_rectangle_box(2, 1, 1, 0.2)