from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline
import torch
import os

# 모델 경로 설정
model_path = "runwayml/stable-diffusion-v1-5"
embedding_path = "path_to_your_learned_embeds.safetensors"

# 파이프라인 로드
pipe = StableDiffusionPipeline.from_pretrained(
    model_path, torch_dtype=torch.float16
).to("cuda")


# 학습된 임베딩 로드
pipe.load_textual_inversion(embedding_path)

# 프롬프트
prompts = [
    "towering mountains in a traditional Korean ink-and-wash painting in <ink_painting> style",
    "towering mountains and a quiet stream with a small village in a traditional Korean ink-and-wash painting in <ink_painting> style",
    "towering mountains veiled in early morning mist, a quiet stream winding through the valley, with a picturesque village surrounded by blossoming cherry trees and traditional Korean houses, all captured in the intricate and fluid strokes of a traditional ink-and-wash painting in <ink_painting> style"
]

# 이미지 생성 루프
for i, prompt in enumerate(prompts):
    folder_name = f"prompt_{i+1}_images"
    save_dir = os.path.join("path_to_generated_images_folder", folder_name)
    os.makedirs(save_dir, exist_ok=True)

    print(f"{folder_name} 폴더에 이미지 저장 시작...")
    
    for j in range(1, 31):
        # 이미지 생성
        image = pipe(prompt).images[0]
        image_path = os.path.join(save_dir, f"image_{j}.png")
        image.save(image_path)
        print(f"이미지가 '{image_path}'로 저장되었습니다.")

    print(f"{folder_name} 폴더에 모든 이미지 저장 완료.")
