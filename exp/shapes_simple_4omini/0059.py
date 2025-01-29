import bpy
import math

def create_rectangle_with_semicircle(width, height, semicircle_radius):
    # Create the rectangle
    bpy.ops.mesh.primitive_plane_add(size=width, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    rectangle = bpy.context.object
    rectangle.name = "Rectangle"
    
    # Scale the rectangle to the desired height
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(1, 1, height))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create the semicircle
    bpy.ops.mesh.primitive_circle_add(radius=semicircle_radius, fill_type='NOTHING', location=(0, 0, height))
    semicircle = bpy.context.object
    semicircle.name = "Semicircle"
    
    # Scale the semicircle to fit the rectangle width
    semicircle.scale[0] = width / 2
    
    # Move the semicircle up to sit on top of the rectangle
    semicircle.location.z += semicircle_radius

    # Join the rectangle and semicircle
    bpy.ops.object.select_all(action='DESELECT')
    rectangle.select_set(True)
    semicircle.select_set(True)
    bpy.context.view_layer.objects.active = rectangle
    bpy.ops.object.join()

create_rectangle_with_semicircle(2, 1, 1)