import gdown
import json
import os

# ID file index.json của bạn
MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    # Xóa file cũ nếu tồn tại để tải bản mới nhất về
    if os.path.exists("index.json"):
        os.remove("index.json")
    
    # Tải file từ Drive
    url = f'https://drive.google.com/uc?id={MASTER_ID}'
    gdown.download(url, "index.json", quiet=False, fuzzy=True)
    
    # Đọc file
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_lesson_content(file_id):
    output = "lesson.json"
    if os.path.exists(output):
        os.remove(output)
    
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output, quiet=False, fuzzy=True)
    
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)