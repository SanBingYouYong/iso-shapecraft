import os
import torch
import clip
from PIL import Image
import re

PREFIX = "A raw mesh rendering of "

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
        # Optionally, you can multiply by a scaling factor (e.g., 100) if needed.
        similarity = (image_features @ text_features.T).squeeze().item()
        similarity_scores[png_file] = similarity

    return similarity_scores

# --- Example usage ---
if __name__ == "__main__":
    # Replace with the path to your folder
    folder = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini\shape_0000\\aggregator"
    scores = compute_clip_similarity(folder)
    for image_file, score in scores.items():
        print(f"{image_file}: similarity score = {score:.4f}")
