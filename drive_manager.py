import gdown
import json
import os

MASTER_ID = "YOUR_MASTER_INDEX_ID" # THAY ID VÀO ĐÂY

def get_master_index():
    if not os.path.exists("master.json"):
        gdown.download(f'https://drive.google.com/uc?id={MASTER_ID}', "master.json", quiet=False)
    with open("master.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_lesson_content(grade, unit):
    index = get_master_index()
    file_id = index.get(grade, {}).get(unit)
    output = "lesson.json"
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False, fuzzy=True)
    with open(output, "r", encoding="utf-8") as f:
        return json.load(f)