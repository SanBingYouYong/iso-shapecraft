import bpy
import bmesh

def create_rhombus(size=1):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Rhombus")
    obj = bpy.data.objects.new("Rhombus", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh object
    bm = bmesh.new()

    # Define the vertices of the rhombus (2D)
    v1 = bm.verts.new((0, size, 0))
    v2 = bm.verts.new((size, 0, 0))
    v3 = bm.verts.new((0, -size, 0))
    v4 = bm.verts.new((-size, 0, 0))

    # Create faces (two triangles to form a rhombus)
    bm.faces.new((v1, v2, v3))
    bm.faces.new((v1, v3, v4))

    # Update the mesh with the bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the origin to the geometry center
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

create_rhombus(size=1)