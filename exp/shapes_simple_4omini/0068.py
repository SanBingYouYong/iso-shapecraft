import bpy
import bmesh

def create_rounded_rectangle(width, height, depth, radius):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object
    obj.dimensions = (width, height, depth)
    
    # Create a BMesh to work with the geometry
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    
    # Add a rounded effect to the corners
    for v in bm.verts:
        if abs(v.co.x) >= width / 2 - radius and abs(v.co.y) >= height / 2 - radius:
            v.co.z -= depth / 2
        else:
            v.co.z += depth / 2

    # Create rounded corners
    bmesh.ops.bevel(bm, geom=bm.verts, offset=radius)
    
    # Write the BMesh back to the mesh
    bm.to_mesh(obj.data)
    bm.free()

# Parameters for the rounded rectangle
width = 2
height = 1
depth = 0.5
radius = 0.2

create_rounded_rectangle(width, height, depth, radius)