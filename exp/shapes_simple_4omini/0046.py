import bpy

def create_cutout_square():
    # Remove all existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the outer square
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=True)
    outer_square = bpy.context.object
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Create the inner square (cutout)
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=True)
    inner_square = bpy.context.object
    inner_square.location = (1, -1, 0)  # Move cutout to corner
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Go back to the outer square and perform the cut
    bpy.context.view_layer.objects.active = outer_square
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    outer_square.data.polygons[0].select = True
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Boolean modifier for cutout
    modifier = outer_square.modifiers.new(name="Boolean", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.use_self = True
    modifier.object = inner_square
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Delete the inner square
    bpy.data.objects.remove(inner_square)

create_cutout_square()