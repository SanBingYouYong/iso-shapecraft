import os
import torch
import clip
from PIL import Image
import re
import numpy as np
from collections import defaultdict

PREFIX = "Raw mesh rendering of "

def parse_shape_file(file_path):
    parsed_data = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    shape_match = re.search(r"shape to be modeled:\s*(.*)", content, re.IGNORECASE)
    description_match = re.search(r"shape description:\s*(.*)", content, re.IGNORECASE | re.DOTALL)
    
    if shape_match:
        parsed_data['shape'] = shape_match.group(1).strip()
    if description_match:
        parsed_data['description'] = description_match.group(1).strip()
    
    return parsed_data

def compute_clip_similarity(folder_path):
    """
    Given a folder path containing one text file (with a shape description)
    and one or more PNG image files, this function uses CLIP to compute
    a similarity score between the text and each image.
    
    Args:
        folder_path (str): Path to the folder containing the txt and png files.
        
    Returns:
        dict: A dictionary mapping each PNG filename to its similarity score.
    """
    # --- Locate the text file ---
    txt_path = os.path.join(folder_path, "shape_description.txt")
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Text file not found in {folder_path}")
    with open(txt_path, 'r', encoding='utf-8') as file:
        text_description = file.read().strip()
    try:
        parsed = parse_shape_file(txt_path)['shape']
        if parsed:
            text_description = parsed
    except Exception as e:
        pass
    text_description = PREFIX + text_description

    # --- Set up CLIP ---
    # Choose the device: use CUDA if available, otherwise CPU.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Load the CLIP model and its preprocessing function.
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Tokenize and encode the text description.
    text_tokens = clip.tokenize([text_description]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)  # Normalize the text features

    # --- Process each PNG image ---
    similarity_scores = {}
    png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    for png_file in png_files:
        image_path = os.path.join(folder_path, png_file)
        # Open and convert the image to RGB.
        image = Image.open(image_path).convert("RGB")
        # Preprocess the image for CLIP.
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)  # Normalize the image features
        
        # Compute cosine similarity (the dot product of the normalized vectors).
        # Optionally, you can multiply by a scaling factor ([ e.g., 100) if needed.
        similarity = (image_features @ text_features.T).squeeze().item()
        similarity_scores[png_file] = similarity

    return similarity_scores

def calcstat_clip_forall(root_folder):
    '''
    For all subfolders, write each image's similarity score to a file 
    '''
    # --- Set up CLIP ---
    # Choose the device: use CUDA if available, otherwise CPU.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Load the CLIP model and its preprocessing function.
    model, preprocess = clip.load("ViT-B/32", device=device)

    txt_file = 'shape_description.txt'
    paths = []
    for root, dirs, files in os.walk(root_folder):
        if txt_file in files and any(f.endswith('.png') for f in files):
            paths.append(root)
    for folder in paths:
        print(folder)
        # scores = compute_clip_similarity(folder)
        text_file = os.path.join(folder, 'shape_description.txt')
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as file:
            text_description = file.read().strip()
        try:
            parsed = parse_shape_file(text_file)['shape']
            if parsed:
                text_description = parsed
        except Exception as e:
            pass
        text_description = PREFIX + text_description

        # Tokenize and encode the text description.
        text_tokens = clip.tokenize([text_description]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            
        # --- Process each PNG image ---
        similarity_scores = {}
        png_files = [f for f in os.listdir(folder) if f.lower().endswith('.png')]
        for png_file in png_files:
            image_path = os.path.join(folder, png_file)
            # Open and convert the image to RGB.
            image = Image.open(image_path).convert("RGB")
            # Preprocess the image for CLIP.
            image_input = preprocess(image).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image_input)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            
            # Compute cosine similarity (the dot product of the normalized vectors).
            similarity = (image_features @ text_features.T).squeeze().item()
            similarity_scores[png_file] = similarity

        with open(os.path.join(folder, 'clip_similarity.yml'), 'w') as f:
            for image_file, score in similarity_scores.items():
                f.write(f"{image_file}: {score}\n")

def check_completion(root_folder):
    '''
    Check if all subfolders have a clip_similarity.yml file
    '''
    txt_file = 'shape_description.txt'
    target_file = 'clip_similarity.yml'
    paths = []
    for root, dirs, files in os.walk(root_folder):
        if txt_file in files and any(f.endswith('.png') for f in files):
            if target_file not in files:
                paths.append(root)
    return paths

# def collect_ymls(root_folder, collect_to: str="./iteration_similarities.yml"):
#     '''
#     Collect all yml files in the root folder
#     '''
#     yml_file = 'clip_similarity.yml'
#     all_stats = {}
#     for root, dirs, files in os.walk(root_folder):
#         if yml_file in files:
#             with open(os.path.join(root, yml_file), 'r') as f:
#                 stats = f.readlines()
#                 all_stats[root] = stats
#     if collect_to:
#         with open(collect_to, 'w') as f:
#             for path, stats in all_stats.items():
#                 f.write(f"{path}:\n")
#                 for stat in stats:
#                     f.write(stat)

def compute_iteration_average_similarity(folder_path, iteration_images):
    shape_file = os.path.join(folder_path, "shape_description.txt")
    if not os.path.exists(shape_file):
        raise FileNotFoundError(f"Shape description file not found in {folder_path}")
    with open(shape_file, 'r', encoding='utf-8') as file:
        text_description = file.read().strip()
    try:
        parsed = parse_shape_file(shape_file)['shape']
        if parsed:
            text_description = parsed
    except Exception as e:
        pass
    text_description = PREFIX + text_description

    # --- Set up CLIP ---
    # Choose the device: use CUDA if available, otherwise CPU.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Load the CLIP model and its preprocessing function.
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Tokenize and encode the text description.
    text_tokens = clip.tokenize([text_description]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)  # Normalize the text features

    # --- Process each PNG image ---
    similarity_scores = {}
    for png_file in iteration_images:
        image_path = os.path.join(folder_path, png_file)
        # Open and convert the image to RGB.
        image = Image.open(image_path).convert("RGB")
        # Preprocess the image for CLIP.
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        # Compute cosine similarity (the dot product of the normalized vectors).
        similarity = (image_features @ text_features.T).squeeze().item()
        similarity_scores[png_file] = similarity

    # Compute the average similarity score for the iteration
    avg_similarity = np.mean(list(similarity_scores.values()))
    return avg_similarity

def similarity_analytics(similarity_scores: list | dict):
    '''
    Given a list of similarity scores, this function computes a series of statistics: 
    - mean, median, std, variance, min/max, percentiles (25th, 75th)

    if received a dict, will convert its values to a list first
    '''
    if isinstance(similarity_scores, dict):
        similarity_scores = list(similarity_scores.values())
    similarity_scores = np.array(similarity_scores)
    mean = np.mean(similarity_scores)
    median = np.median(similarity_scores)
    std = np.std(similarity_scores)
    variance = np.var(similarity_scores)
    min_score = np.min(similarity_scores)
    max_score = np.max(similarity_scores)
    percentile_25th = np.percentile(similarity_scores, 25)
    percentile_75th = np.percentile(similarity_scores, 75)
    
    return {
        "mean": mean,
        "median": median,
        "std": std,
        "variance": variance,
        "min": min_score,
        "max": max_score,
        "25th_percentile": percentile_25th,
        "75th_percentile": percentile_75th
    }

def extract_paths(folder_path):
    """
    Organize image files of format {path}_{iteration}_{id}.png into a nested dictionary structure.
    Handles non-padded numbers in filenames (e.g., 0_1_1.png)
    
    Args:
        folder_path (str): Path to the folder containing the image files
        
    Returns:
        dict: Nested dictionary with structure {path: {iteration: [files]}}
        Example:
        {
            '0': {
                '1': ['0_1_1.png', '0_1_2.png'],
                '2': ['0_2_1.png']
            },
            '1': {
                '1': ['1_1_1.png']
            }
        }
    """
    # Initialize nested defaultdict to automatically create inner dictionaries
    organized_files = defaultdict(lambda: defaultdict(list))
    
    # Updated pattern for non-padded numbers
    pattern = r'(\d+)_(\d+)_(\d+)\.png$'
    
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if not filename.endswith('.png'):
            continue
            
        match = re.match(pattern, filename)
        if match:
            path_prefix, iteration, _ = match.groups()
            organized_files[path_prefix][iteration].append(filename)
    
    # Convert defaultdict to regular dict for cleaner output
    return {
        path: dict(iterations)
        for path, iterations in organized_files.items()
    }

def collect_paths(root_folder):
    '''
    Extract paths from all subfolders in the root folder, for subfolders containing image files and txt file
    '''
    txt_file = 'shape_description.txt'
    paths = {}
    for root, dirs, files in os.walk(root_folder):
        if txt_file in files and any(f.endswith('.png') for f in files):
            paths[root] = extract_paths(root)
    return paths

def check_iterations(root_folder):
    paths = collect_paths(root_folder)
    for folder, data in paths.items():
        for path, iterations in data.items():
            print(f"{folder}: {path} -> {len(iterations)} iterations")

def calcstat_iteration_aves(root_folder):
    paths = collect_paths(root_folder)
    for folder, data in paths.items():
        for path, iterations in data.items():
            print(path, iterations)
            iteration_images = iterations['0']
            print(
                f"{folder}: {path} -> {compute_iteration_average_similarity(folder, iteration_images)}"
            )
    # NOTE: change to use batch processing

# --- Example usage ---
if __name__ == "__main__":
    # folder = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini\shape_0000\\aggregator"
    # scores = compute_clip_similarity(folder)
    # for image_file, score in scores.items():
    #     print(f"{image_file}: similarity score = {score:.4f}")

    # print(extract_paths("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini/shape_0000/aggregator")['0'])

    # print(collect_paths("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini/shape_0000").keys())

    # check_iterations("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini")
    
    # folder_path = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini\shape_0000\\aggregator"
    # iteration_images = extract_paths(folder_path)['0']['0']
    # print(
    #     compute_iteration_average_similarity(
    #         folder_path, iteration_images
    #     )
    # )

    # calcstat_iteration_aves("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini")

    paths = [
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_single_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_10x_shapes_daily_4omini",        
    ]

    # for path in paths:
    #     calcstat_clip_forall(path)

    # for path in paths:
    #     print(check_completion(path))

    # for path in paths:
    #     print(collect_ymls(path))

    # calcstat_clip_forall("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini")
