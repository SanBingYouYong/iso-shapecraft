import bpy
import bmesh

def create_wedge(base_length, height, depth):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # Create a bmesh to modify the cube into a wedge
    bm = bmesh.new()
    bmesh.ops.create_cube(bm)
    
    # Scale the cube to form a wedge
    for v in bm.verts:
        if v.co.x < 0:
            v.co.x *= (base_length / 2)
        v.co.z *= (height)
        v.co.y *= (depth)
    
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x < 0])
    
    # Create the mesh
    mesh = bpy.data.meshes.new("WedgeMesh")
    bm.to_mesh(mesh)
    bm.free()
    
    # Create an object with the mesh
    wedge_object = bpy.data.objects.new("Wedge", mesh)
    bpy.context.collection.objects.link(wedge_object)
    return wedge_object

create_wedge(base_length=2, height=1, depth=1)