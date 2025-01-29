import bpy

def create_flag_with_stripes():
    # Remove existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a plane for the flag
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    flag = bpy.context.active_object
    flag.name = "Flag"

    # Create three stripes
    stripe_height = 0.2
    colors = [(1, 0, 0), (1, 1, 1), (0, 0, 1)]  # Red, White, Blue

    for i in range(3):
        # Create a new material for each stripe
        mat = bpy.data.materials.new(name=f"Stripe_{i+1}")
        mat.diffuse_color = (*colors[i], 1)  # RGBA
        flag.data.materials.append(mat)

        # Create a stripe
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, (i - 1) * stripe_height))
        stripe = bpy.context.active_object
        stripe.name = f"Stripe_{i + 1}"
        stripe.data.materials.append(mat)

        # Scale the stripe to make it long
        stripe.scale[1] = 1.5

    # Combine all stripes into one object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.context.view_layer.objects.active = flag
    bpy.ops.object.join()

create_flag_with_stripes()