import os


def count_obj_vertices_faces(obj_file_path):
    """
    读取OBJ文件并返回顶点数和面数。
    
    参数:
        obj_file_path (str): OBJ文件的路径
        
    返回:
        tuple: (顶点数, 面数)
    """
    vertices = 0
    faces = 0
    
    with open(obj_file_path, 'r') as file:
        for line in file:
            # 去除前后空白并分割
            stripped_line = line.strip()
            if not stripped_line:
                continue  # 跳过空行
            
            # 检查顶点行（以'v '开头）
            if stripped_line.startswith('v '):
                vertices += 1
            # 检查面行（以'f '开头）
            elif stripped_line.startswith('f '):
                faces += 1
                
    return vertices, faces

def find_obj_and_count(folder_path):
    """
    查找文件夹中的所有OBJ文件并返回它们的顶点数和面数。
    
    参数:
        folder_path (str): 包含OBJ文件的文件夹路径
        
    返回:
        dict: 包含文件名和对应顶点数和面数的字典
    """
    obj_counts = {}
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.obj'):
                obj_file_path = os.path.join(root, file)
                v_count, f_count = count_obj_vertices_faces(obj_file_path)
                obj_counts[obj_file_path] = (v_count, f_count)
                
    return obj_counts

from pathlib import Path
import re

def extract_scad_experiment(root_folder):
    """
    Walks through each shape_xxxx folder in `root_folder` and extracts the required files.
    
    Returns a dictionary keyed by the shape index (i.e. the padded number from the folder name)
    with a dictionary of file paths for each file.
    """
    results = {}

    # Look for all directories that start with "shape_"
    root = Path(root_folder)
    for shape_dir in root.glob("shape_*"):
        if not shape_dir.is_dir():
            continue

        # Extract the padded index (i) from folder name: "shape_0001" -> "0001"
        try:
            shape_index = shape_dir.name.split("_")[1]
        except IndexError:
            continue

        # Prepare a dictionary to hold the files for this shape
        data = {
            "obj": None,
            "scad": None,
            "history": None,
            "png": {},  # Will hold keys '0'..'3'
            "evaluation_history": None,
            "evaluation_prompt": None,
            "evaluations": None,
            "shape_description": None,
        }

        # Loop over all files in the folder
        for f in shape_dir.iterdir():
            name = f.name

            # Match {i}_{j}.obj
            if re.fullmatch(rf"{shape_index}_(\d+)\.obj", name):
                data["obj"] = f

            # Match {i}_{j}.scad
            elif re.fullmatch(rf"{shape_index}_(\d+)\.scad", name):
                data["scad"] = f

            # Match {i}_history.json
            elif name == f"{shape_index}_history.json":
                data["history"] = f

            # Match {i}_{j}_{k}.png with k in [0-3]
            elif re.fullmatch(rf"{shape_index}_(\d+)_([0-3])\.png", name):
                m = re.fullmatch(rf"{shape_index}_(\d+)_([0-3])\.png", name)
                if m:
                    k = m.group(2)  # k is one of "0", "1", "2", or "3"
                    data["png"][k] = f

            # The following files do not depend on the shape index
            elif name == "evaluation_history.json":
                data["evaluation_history"] = f
            elif name == "evaluation_prompt.md":
                data["evaluation_prompt"] = f
            elif name == "evaluations.json":
                data["evaluations"] = f
            elif name == "shape_description.txt":
                data["shape_description"] = f

        results[shape_index] = data

    return results

# 使用示例
if __name__ == "__main__":
    # file_path = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scad_exp_3x_shapes_daily_4omini\shape_0000\855161a1aaba30c2b4b1aa7f729e2961\e403e5c5cc19a213991df87c33a2b180.obj"  # 替换为你的OBJ文件路径
    # v_count, f_count = count_obj_vertices_faces(file_path)
    # print(f"顶点数: {v_count}, 面数: {f_count}")
    # counts = find_obj_and_count("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scad_exp_3x_shapes_daily_4omini")  # 替换为你的文件夹路径
    # print(f"找到{len(counts)}个OBJ文件")
    # average_v_count = sum(v_count for v_count, _ in counts.values()) / len(counts)
    # average_f_count = sum(f_count for _, f_count in counts.values()) / len(counts)
    # print(f"平均顶点数: {average_v_count}, 平均面数: {average_f_count}")

    folder_path = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_10x_shapes_daily_4omini"  # Change this to the path of your folder containing the shape_xxxx directories
    extracted_files = extract_scad_experiment(folder_path)
    
    # Print out the found files for each shape folder:
    for shape_index, files in extracted_files.items():
        print(f"Shape {shape_index}:")
        print(f"  OBJ file:             {files['obj']}")
        print(f"  SCAD file:            {files['scad']}")
        print(f"  History file:         {files['history']}")
        print("  PNG files:")
        for k in sorted(files['png']):
            print(f"    k={k}: {files['png'][k]}")
        print(f"  Evaluation history:   {files['evaluation_history']}")
        print(f"  Evaluation prompt:    {files['evaluation_prompt']}")
        print(f"  Evaluations:          {files['evaluations']}")
        print(f"  Shape description:    {files['shape_description']}")
        print("-" * 40)
        # raise

