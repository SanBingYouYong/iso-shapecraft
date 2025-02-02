import bpy
import bmesh
from mathutils import Vector

def create_pizza_slice():
    # Parameters for the pizza slice
    radius = 1.0
    crust_thickness = 0.2
    slice_angle = 60  # degrees
    slice_height = 0.2

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name="PizzaSlice")
    obj = bpy.data.objects.new("PizzaSlice", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the geometry
    bm = bmesh.new()

    # Create the outer edge vertices (crust)
    outer_verts = []
    for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
        rad = (angle * 3.14159) / 180
        x = radius * Vector((1, 0, 0)).rotate(Vector((0, 0, rad)))
        z = Vector((0, 0, crust_thickness))
        outer_verts.append(bm.verts.new(x + z))

    # Create the inner edge vertices (topping)
    inner_verts = []
    for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
        rad = (angle * 3.14159) / 180
        x = (radius - crust_thickness) * Vector((1, 0, 0)).rotate(Vector((0, 0, rad)))
        inner_verts.append(bm.verts.new(x))

    # Create faces for the pizza slice
    for i in range(len(outer_verts) - 1):
        bm.faces.new((outer_verts[i], outer_verts[i+1], inner_verts[i+1], inner_verts[i]))

    # Create the tip face
    bm.faces.new((inner_verts[0], inner_verts[-1], outer_verts[-1], outer_verts[0]))

    # Write the bmesh into the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the object origin to geometry center
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

    # Move the pizza slice up to visualize it better
    obj.location.z += slice_height / 2

create_pizza_slice()