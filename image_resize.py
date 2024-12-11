from PIL import Image
import os

def resize_with_aspect_ratio(image, target_size=(512, 512)):
    image.thumbnail(target_size, Image.ANTIALIAS)
    new_image = Image.new("RGB", target_size, (255, 255, 255))
    paste_position = (
        (target_size[0] - image.size[0]) // 2,
        (target_size[1] - image.size[1]) // 2
    )
    new_image.paste(image, paste_position)
    return new_image

input_folder = "path_to_image"
output_folder = "path_to_output_folder"
os.makedirs(output_folder, exist_ok=True)

target_size = (512, 512) 
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")): 
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)
        
        # 비율 유지 리사이즈 실행
        resized_image = resize_with_aspect_ratio(image, target_size)
        
        # 결과 저장
        resized_image.save(os.path.join(output_folder, filename))
        print(f"Resized and saved: {filename}")

print(f"모든 이미지가 {output_folder}에 저장되었습니다.")