import os
import re
import yaml

def collect_folder_data(root_folder, output_yml_path):
    """
    收集指定根目录下所有8位数字命名子文件夹的特定文件信息，并写入YAML文件
    
    参数:
    root_folder (str): 要扫描的根目录绝对路径
    output_yml_path (str): 输出YAML文件的绝对路径
    """
    
    # 初始化数据字典
    collected_data = {}

    try:
        # 验证根目录是否存在
        if not os.path.isdir(root_folder):
            raise ValueError(f"指定的根目录不存在: {root_folder}")

        # 遍历根目录下的所有项目
        for entry in os.listdir(root_folder):
            folder_path = os.path.join(root_folder, entry)
            
            # 检查是否为8位数字命名的文件夹
            if os.path.isdir(folder_path) and re.fullmatch(r'^\d{8}$', entry):
                folder_data = {}
                
                try:
                    # 获取绝对路径
                    abs_folder_path = os.path.abspath(folder_path)
                    folder_data["folder_path"] = abs_folder_path

                    # 处理Ground Truth.obj路径
                    gt_obj_path = os.path.join(folder_path, "Ground_Truth.obj")
                    if os.path.isfile(gt_obj_path):
                        folder_data["ground_truth_obj"] = os.path.abspath(gt_obj_path)
                    else:
                        folder_data["ground_truth_obj"] = None

                    # 读取文本文件内容
                    text_files = {
                        "natural_language_prompt": "Natural_Language_Descriptions_Prompt.txt",
                        "natural_language_measurements": "Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
                    }

                    for key, filename in text_files.items():
                        file_path = os.path.join(folder_path, filename)
                        if os.path.isfile(file_path):
                            with open(file_path, "r", encoding="utf-8") as f:
                                folder_data[key] = f.read().strip()
                        else:
                            folder_data[key] = None

                    # 将数据添加到主字典
                    collected_data[entry] = folder_data

                except Exception as e:
                    print(f"处理文件夹 {entry} 时出错: {str(e)}")
                    continue

        # 写入YAML文件
        with open(output_yml_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(collected_data, yaml_file, allow_unicode=True)

        print(f"成功导出数据到: {output_yml_path}")
        return True

    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        return False

SPLIT_CANDIDATES = [
    "write a python code using CADQuery to create",
    "write a python script using CADQuery to create",
    "Write Python code using CADQuery to create",
    "Write Python code using CADQuery to generate",
    "Write Python code using CADQuery for",
    "Write Python code with CADQuery to create"
    # NOTE: manually inserted "created" to that entry
    # "Write Python code using CADQuery to"  # only 00019066... did they manually typed in shape description???
]

def parse_shape_description(input_yml_path, output_yml_path):
    """
    处理YAML文件, 解析natural_language_prompt字段并生成新字段
    
    参数:
    input_yml_path (str): 输入YAML文件绝对路径
    output_yml_path (str): 输出YAML文件绝对路径
    """
    
    try:
        # 读取YAML文件
        with open(input_yml_path, 'r', encoding='utf-8') as yaml_file:
            data = yaml.safe_load(yaml_file) or {}

        # 处理每个条目
        for entry_id, entry_data in data.items():
            if not isinstance(entry_data, dict):
                continue

            prompt = entry_data.get('natural_language_prompt')
            if not prompt:
                print(f"未找到自然语言提示: {entry_id}")
                continue
            split_prefix = None
            for candidate in SPLIT_CANDIDATES:
                if candidate.lower() in prompt.lower():
                    split_prefix = candidate
                    break
            
            if not split_prefix:
                print(f"未找到分割前缀: {entry_id} | {prompt}")
                continue

            # 解析文本
            if prompt and split_prefix in prompt:
                # 分割字符串（最多分割一次）
                parts = prompt.split(split_prefix, 1)
                entry_data['parsed_shape_description'] = parts[1].strip() if len(parts) > 1 else None
            else:
                entry_data['parsed_shape_description'] = None

        # 写回新文件
        with open(output_yml_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False, allow_unicode=True)

        print(f"成功处理并保存到: {output_yml_path}")
        return True

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        return False

# 使用示例
if __name__ == "__main__":
    # root = "C:\ZSY\imperial\courses\ISO\CAD_Code_Generation\CADPrompt"  # 替换为实际根目录
    # output = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\dataset\cadprompt.yml"   # 替换为实际输出目录
    # collect_folder_data(root, output)
    parse_shape_description("./dataset/cadprompt.yml", "./dataset/cadprompt_parsed.yml")