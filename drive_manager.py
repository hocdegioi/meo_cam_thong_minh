import gdown
import json
import os

def get_master_index(master_id):
    # Tải file index.json về máy tính
    if os.path.exists("index.json"):
        os.remove("index.json")
    url = f'https://drive.google.com/uc?id={master_id}'
    gdown.download(url, "index.json", quiet=False)
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_lesson_content(file_id):
    # Tải file bài học dựa trên file_id nhận được
    output = "lesson.json"
    if os.path.exists(output):
        os.remove(output)
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output, quiet=False, fuzzy=True)
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)