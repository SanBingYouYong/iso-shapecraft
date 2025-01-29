import bpy
import bmesh

def create_musical_note():
    # Create a new mesh
    mesh = bpy.data.meshes.new("MusicalNote")
    obj = bpy.data.objects.new("MusicalNote", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to build the note shape
    bm = bmesh.new()
    
    # Define the note's geometry
    # Creating the circular part of the note
    bmesh.ops.create_circle(bm, cap_tris=True, radius=0.5, location=(0, 0, 0))
    
    # Extrude the circle to create the body of the note
    for v in bm.verts:
        v.co.z += 1  # Height of the note
    
    # Create the stem of the note
    stem_verts = [
        (0, 0, 1),  # Base of the stem
        (0, -0.1, 2),  # Top of the stem
        (0, 0.1, 2),  # Top of the stem (opposite side)
    ]
    
    stem_faces = [(0, 1, 2)]
    
    # Create and add the stem geometry
    stem_mesh = bpy.data.meshes.new("NoteStem")
    stem_obj = bpy.data.objects.new("NoteStem", stem_mesh)
    
    bpy.context.collection.objects.link(stem_obj)
    
    # Create the stem mesh
    stem_mesh.from_pydata(stem_verts, [], stem_faces)
    stem_mesh.update()

    # Combine the note and the stem into one object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    stem_obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()

    # Cleanup
    bmesh.update_edit_mesh(mesh)
    bm.free()

create_musical_note()