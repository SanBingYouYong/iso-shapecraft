import bpy
import math

def create_u_shaped_curve(radius=1, height=1, segments=32):
    # Create a new curve
    curve_data = bpy.data.curves.new('UShapeCurve', type='CURVE')
    curve_data.dimensions = '3D'
    
    # Create a new spline
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(segments - 1)

    # Set the points for the U shape
    for i in range(segments):
        angle = math.pi * (i / (segments - 1))  # U shape from 0 to ¦Ð
        x = radius * math.sin(angle)
        y = radius * (1 - math.cos(angle))  # Offset to create the U shape
        spline.bezier_points[i].co = (x, y, 0)
        spline.bezier_points[i].handle_left_type = 'AUTO'
        spline.bezier_points[i].handle_right_type = 'AUTO'
    
    # Create an object with the curve
    curve_object = bpy.data.objects.new('UShapeCurveObject', curve_data)
    
    # Link the object to the current scene
    bpy.context.collection.objects.link(curve_object)

create_u_shaped_curve()