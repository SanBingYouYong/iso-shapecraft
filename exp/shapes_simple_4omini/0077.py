import bpy

def create_rectangle_with_circular_hole(length, width, hole_diameter):
    # Create a rectangle
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=True)
    bpy.ops.transform.resize(value=(length / 2, width / 2, 1))
    
    # Go to edit mode to create the hole
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.primitive_circle_add(radius=hole_diameter / 2, location=(0, 0, 0))
    bpy.ops.mesh.intersect_boolean(operation='DIFFERENCE')
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Clean up: remove the original circle object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.data.objects['Circle'].select_set(True)
    bpy.ops.object.delete()

# Parameters: length, width, hole diameter
create_rectangle_with_circular_hole(4, 2, 1)