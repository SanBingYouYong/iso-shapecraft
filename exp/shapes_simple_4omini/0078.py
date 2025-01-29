import bpy
import math

def create_curved_arc(radius, angle, segments):
    # Create a new curve object
    curve_data = bpy.data.curves.new(name='CurvedArc', type='CURVE')
    curve_data.dimensions = '3D'
    
    # Create a polyline for the curve
    polyline = curve_data.splines.new('BEZIER')
    polyline.bezier_points.add(segments - 1)
    
    # Calculate points for the arc
    for i in range(segments):
        theta = angle * (i / (segments - 1))  # Angle for each segment
        x = radius * math.cos(theta)  # X position
        y = radius * math.sin(theta)  # Y position
        polyline.bezier_points[i].co = (x, y, 0)  # Set point coordinates

    # Create an object with the curve data
    curve_object = bpy.data.objects.new('CurvedArcObject', curve_data)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(curve_object)

# Parameters for the arc
create_curved_arc(radius=5, angle=math.radians(90), segments=10)