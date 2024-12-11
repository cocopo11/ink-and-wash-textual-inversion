import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from torch.nn.functional import cosine_similarity

def calculate_clip_score(image_path, prompt):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to("cuda")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=prompt, images=image, return_tensors="pt", padding=True).to("cuda")

    with torch.no_grad():
        outputs = model(**inputs)
        image_features = outputs.image_embeds
        text_features = outputs.text_embeds
        score = cosine_similarity(image_features, text_features).item()
    return score

if __name__ == "__main__":
    image_path = "path_to_your_generated_image.png"
    prompt = "prompt_of_your_image"
    score = calculate_clip_score(image_path, prompt)
    print(f"Image: {image_path}, Prompt: {prompt}, CLIP Score: {score:.4f}")