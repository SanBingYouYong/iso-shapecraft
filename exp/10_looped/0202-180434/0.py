import bpy

def create_charging_cable(length=5.0, width=0.1, height=0.1):
    # Create a rectangular prism (cable)
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    cable = bpy.context.object
    cable.scale = (length / 2, width / 2, height / 2)
    
    # Rename the object to 'Charging Cable'
    cable.name = 'Charging Cable'

create_charging_cable()