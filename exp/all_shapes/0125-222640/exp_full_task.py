import bpy
import math

def create_undulating_plane(width, depth, amplitude, wavelength):
    # Create a rectangular plane
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane = bpy.context.object
    plane.scale = (width / 2, depth / 2, 1)
    
    # Enter edit mode to modify the vertices
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(plane.data)
    
    # Undulate the plane using a sine wave
    for v in mesh.verts:
        x = v.co.x
        v.co.z = amplitude * math.sin((x / wavelength) * (2 * math.pi))
    
    # Update the mesh and return to object mode
    bmesh.update_edit_mesh(plane.data)
    bpy.ops.object.mode_set(mode='OBJECT')

create_undulating_plane(20, 15, 2, 5)