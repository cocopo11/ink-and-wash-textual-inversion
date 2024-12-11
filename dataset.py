import os
import json
import pandas as pd

# 경로 설정
base_path = "path_to_caption_data"  # 압축 해제된 폴더 루트 경로
output_csv_path = "path_to_dataset.csv"
image_base_path = os.path.join(base_path, "path_to_image")

# 이미지 파일 검색 함수
def find_image(image_name, base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == image_name:
                return os.path.join(root, file)
    return None

# 통합 데이터셋 생성
combined_dataset = []

# JSON 파일 리스트 가져오기
json_files = []
for root, _, files in os.walk(base_path):
    for file_name in files:
        if file_name.endswith(".json"):
            json_files.append(os.path.join(root, file_name))

total_files = len(json_files)  # 총 파일 수
print(f"총 {total_files}개의 JSON 파일을 처리합니다.")

# JSON 파일 처리
for idx, file_path in enumerate(json_files, start=1):
    with open(file_path, 'r', encoding='utf-8') as file:
        labels = json.load(file)
        images_data = labels.get("images", {})

        # 이미지 이름
        image_name = images_data.get("identifier", "")

        # 이미지 파일 경로 검색
        image_path = find_image(image_name, image_base_path)

        record = {
            "file_name": os.path.basename(file_path),
            "image_name": image_name,
            "image_path": image_path if image_path else "Not Found",
            "caption_kr": images_data.get("caption_kr", ""),
            "caption_en": images_data.get("caption_en", "")
        }

        # 이미지가 없으면 로그 남기기
        if image_path:
            combined_dataset.append(record)
        else:
            print(f"[{idx}/{total_files}] Image not found: {image_name} (Skipping)")

    # 진행 상황 출력
    print(f"[{idx}/{total_files}] JSON 파일 처리 완료: {os.path.basename(file_path)}")

# 데이터프레임으로 변환 및 CSV 저장
combined_df = pd.DataFrame(combined_dataset)
combined_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

print(f"통합 캡션 데이터셋이 '{output_csv_path}'에 저장되었습니다.")



