import bpy
import math

def create_butterfly_wings():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the left wing
    bpy.ops.mesh.primitive_bezier_curve_add(location=(-1, 0, 0))
    left_wing = bpy.context.object
    left_wing.data.bevel_depth = 0.1
    left_wing.data.bevel_resolution = 5

    # Adjust control points for the left wing
    left_wing.data.splines[0].bezier_points[0].co = (-1, 0, 0)
    left_wing.data.splines[0].bezier_points[0].handle_right = (-0.5, 0.5, 0)
    left_wing.data.splines[0].bezier_points[0].handle_left = (-0.5, -0.5, 0)
    
    left_wing.data.splines[0].bezier_points[1].co = (0, 1, 0)
    left_wing.data.splines[0].bezier_points[1].handle_right = (0.5, 1, 0)
    left_wing.data.splines[0].bezier_points[1].handle_left = (0.5, 1, 0)

    left_wing.data.splines[0].bezier_points[2].co = (1, 0, 0)
    left_wing.data.splines[0].bezier_points[2].handle_right = (1, -0.5, 0)
    left_wing.data.splines[0].bezier_points[2].handle_left = (1, 0.5, 0)

    # Create the right wing by mirroring the left wing
    bpy.ops.object.duplicate()
    right_wing = bpy.context.object
    right_wing.location.x *= -1

    # Join wings into a single object
    bpy.ops.object.select_all(action='DESELECT')
    left_wing.select_set(True)
    right_wing.select_set(True)
    bpy.context.view_layer.objects.active = left_wing
    bpy.ops.object.join()

    # Add a solidify modifier for thickness
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.1

create_butterfly_wings()