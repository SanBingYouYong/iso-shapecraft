import requests
import torch
from PIL import Image
from transformers import AlignProcessor, AlignModel

processor = AlignProcessor.from_pretrained("kakaobrain/align-base")
model = AlignModel.from_pretrained("kakaobrain/align-base")

image_path = "exp\eval_python_single_10x_shapes_daily_4omini\shape_0000/0_0_0.png"
image = Image.open(image_path).convert("RGB")
candidate_labels = ["Raw mesh rendering of: A cylindrical coffee mug with a handle on the side.", "Raw mesh rendering of: A small cube is positioned slightly to the left of a larger sphere."]

inputs = processor(images=image ,text=candidate_labels, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# this is the image-text similarity score
logits_per_image = outputs.logits_per_image

print(logits_per_image)

# we can take the softmax to get the label probabilities
probs = logits_per_image.softmax(dim=1)
print(probs)