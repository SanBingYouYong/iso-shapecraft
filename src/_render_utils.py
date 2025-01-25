import bpy
import mathutils
import sys
import math

"""
Automatically render the intended collections with the specified camera and specs, one collection at a time. 
Important: Backup your blender file before running this script: it applies all the transformations of your objects! 


Modified upon https://github.com/SanBingYouYong/Blender-Auto-Renderer
"""

def set_camera(camera, x, y, z=1.5):
    """
    Camera is tracked to [0, 0, 0] by default, so only change its x y z coordinates
    """
    camera.location.x = x
    camera.location.y = y
    camera.location.z = z

def calculate_bounding_box_for_collection(collection: str):
    """
    Calculate the bounding box size of the given collection. 
    The reference to the collection must have been updated. 

    Important: It applies all the transformations of your objects! Either undo afterwards, or backup your file.
    If the object has modifiers (e.g. array), it converts it to a mesh! 
    """
    collection = bpy.data.collections[collection]

    min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
    max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")

    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        if obj.name in ["Camera", "Light", "Empty"]:
            continue
        # Make the object the only active one to apply transformation -> to calculate bbox correctly
        obj.select_set(True)
        if obj.modifiers:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.convert(target="MESH")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        for coord in obj.bound_box:
            min_x = min(min_x, coord[0])
            min_y = min(min_y, coord[1])
            min_z = min(min_z, coord[2])
            max_x = max(max_x, coord[0])
            max_y = max(max_y, coord[1])
            max_z = max(max_z, coord[2])
        obj.select_set(False)
    
    objects_width = max_x - min_x
    objects_height = max_y - min_y
    objects_depth = max_z - min_z

    return {
        "min_x": min_x,
        "min_y": min_y,
        "min_z": min_z,
        "max_x": max_x,
        "max_y": max_y,
        "max_z": max_z,
        "width": objects_width,
        "height": objects_height,
        "depth": objects_depth
    }



def calculate_camera(bounding_box):
    # 计算中心
    center_x = (bounding_box['min_x'] + bounding_box['max_x']) / 2
    center_y = (bounding_box['min_y'] + bounding_box['max_y']) / 2
    center_z = (bounding_box['min_z'] + bounding_box['max_z']) / 2

    # 包围盒尺寸
    width = bounding_box['width']
    height = bounding_box['height']
    depth = bounding_box['depth']

    # 包围球半径
    r = math.sqrt((width/2)**2 + (height/2)**2 + (depth/2)**2)

    # 相机方向（右前上方）
    dir_x, dir_y, dir_z = 1.0, 1.0, 1.0
    length = math.sqrt(dir_x**2 + dir_y**2 + dir_z**2)
    dir = (dir_x/length, dir_y/length, dir_z/length)

    # 视场角45度，计算距离
    fov_deg = 45
    fov_rad = math.radians(fov_deg)
    distance = r / math.tan(fov_rad / 2)

    # 相机位置
    camera_x = center_x + dir[0] * distance
    camera_y = center_y + dir[1] * distance
    camera_z = center_z + dir[2] * distance

    return {
        "position": (camera_x, camera_y, camera_z),
        "target": (center_x, center_y, center_z),
        "up": (0, 1, 0),
        "fov": fov_deg
    }

def update_cam(results):
    camera = bpy.data.objects['Camera']
    camera.location.x = results["position"][0]
    camera.location.y = results["position"][1]
    camera.location.z = results["position"][2]
    camera.rotation_euler = mathutils.Vector(results["target"]) - mathutils.Vector(results["position"])
    camera.data.lens = results["fov"]


def remove_all_objects():
    """
    Remove all objects except the camera, light, and emtpy.
    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name in ["Camera", "Light", "Empty"]:
            continue
        obj.select_set(True)
    bpy.ops.object.delete()

def export_obj(filepath):
    """
    Export the current scene as an obj file
    """
    # select all non-camera/light/empty objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name in ["Camera", "Light", "Empty"]:
            continue
        obj.select_set(True)
    # export selected objects
    bpy.ops.wm.obj_export(filepath=filepath)

def select_objects_join_normalize_size(collection: str):
    """
    Select all objects in the collection, join them, and normalize the size
    """
    collection = bpy.data.collections[collection]
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        if obj.name in ["Camera", "Light", "Empty"]:
            continue
        obj.select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj = bpy.context.object
    bbox = obj.bound_box
    min_x = min([coord[0] for coord in bbox])
    max_x = max([coord[0] for coord in bbox])
    min_y = min([coord[1] for coord in bbox])
    max_y = max([coord[1] for coord in bbox])
    min_z = min([coord[2] for coord in bbox])
    max_z = max([coord[2] for coord in bbox])

    scale_x = 2 / (max_x - min_x)
    scale_y = 2 / (max_y - min_y)
    scale_z = 2 / (max_z - min_z)
    scale = min(scale_x, scale_y, scale_z)

    bpy.ops.transform.resize(value=(scale, scale, scale))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.location_clear()


if __name__ == "__main__":
    # print(f"Commencing rendering with {sys.argv}")
    # args = sys.argv[sys.argv.index("--") + 1:]
    # obj_dataset_path, output_folder = args
    # main(obj_dataset_path, output_folder)
    export_obj("~/temp.obj")
