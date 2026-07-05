import gdown
import json
import os

# Đây là ID của file index.json trên Drive của bạn
MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    # Tải file index.json về máy tính để đọc cấu trúc
    if os.path.exists("index.json"):
        os.remove("index.json") # Xóa bản cũ để tải bản mới nhất
    gdown.download(f'https://drive.google.com/uc?id={MASTER_ID}', "index.json", quiet=False)
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_lesson_content(grade, unit):
    index = get_master_index()
    # Lấy ID của file bài học tương ứng với Lớp và Unit đã chọn
    file_id = index.get(grade, {}).get(unit)
    
    if not file_id:
        return {"vocabulary": ["Không tìm thấy bài học!"]}
        
    output = "lesson.json"
    if os.path.exists(output):
        os.remove(output)
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False, fuzzy=True)
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)