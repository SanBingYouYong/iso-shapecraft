import bpy
import math

def create_c_shape(radius, thickness, location):
    # Create a new curve
    bpy.ops.curve.primitive_bezier_curve_add()
    curve = bpy.context.object
    curve.name = "C_Shape"

    # Set curve points
    curve.data.splines.clear()
    spline = curve.data.splines.new(type='BEZIER')
    spline.bezier_points.add(3)

    # Define control points for a C shape
    points = [
        (0, 0, 0),       # Start point
        (radius * 0.5, radius, 0),  # Control point 1
        (radius, radius * 0.5, 0),  # Control point 2
        (radius, 0, 0)              # End point
    ]

    for i, point in enumerate(spline.bezier_points):
        point.co = points[i]
        point.handle_left_type = 'AUTO'
        point.handle_right_type = 'AUTO'

    # Adjust thickness
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, thickness)})
    bpy.ops.object.mode_set(mode='OBJECT')

    # Move the C shape to the specified location
    curve.location = location

# Create a C shape with specified parameters
create_c_shape(radius=2, thickness=0.1, location=(0, 0, 0))