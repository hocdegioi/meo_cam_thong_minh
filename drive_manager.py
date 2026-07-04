import os
import gdown
import json

FOLDER_ID = "1nQ8PxZsy35OZvkJCdsmOGSuW8JalAxeq"
DATA_DIR = "data_storage"

def sync_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    url = f"https://drive.google.com/drive/folders/{FOLDER_ID}"
    gdown.download_folder(url, output=DATA_DIR, quiet=False)

def list_folders(dummy_id=None):
    """Liệt kê danh sách các thư mục Lớp_x có trong data_storage"""
    if not os.path.exists(DATA_DIR):
        return []
    # Lấy danh sách thư mục trong data_storage
    folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
    return [{"name": f} for f in sorted(folders)]

def get_lesson_content(lop, bai):
    file_path = os.path.join(DATA_DIR, lop, bai, "content.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None