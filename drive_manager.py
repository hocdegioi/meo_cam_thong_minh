import gdown
import json
import os

MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    # Tải lại file index mới nhất từ Drive
    if os.path.exists("index.json"):
        os.remove("index.json")
    gdown.download(f'https://drive.google.com/uc?id={MASTER_ID}', "index.json", quiet=False)
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_lesson_content(file_id):
    output = "lesson.json"
    if os.path.exists(output):
        os.remove(output)
    # Tải nội dung bài học dựa trên ID nhận được
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False, fuzzy=True)
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)