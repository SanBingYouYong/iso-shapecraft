import bpy
import math

def create_crescent_moon(radius_outer, radius_inner, location):
    # Create the outer circle (full moon)
    bpy.ops.mesh.primitive_circle_add(radius=radius_outer, location=location)
    outer_circle = bpy.context.object
    
    # Create the inner circle (cutout)
    bpy.ops.mesh.primitive_circle_add(radius=radius_inner, location=(location[0] + radius_outer - radius_inner, location[1], location[2]))
    inner_circle = bpy.context.object
    
    # Join the two circles into one object
    bpy.ops.object.select_all(action='DESELECT')
    outer_circle.select_set(True)
    inner_circle.select_set(True)
    bpy.context.view_layer.objects.active = outer_circle
    bpy.ops.object.join()
    
    # Add a solidify modifier to give thickness to the crescent shape
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.1

# Parameters for the crescent moon shape
outer_radius = 1.0
inner_radius = 0.7
location = (0, 0, 0)

create_crescent_moon(outer_radius, inner_radius, location)