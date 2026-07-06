import gdown
import json
import os
import streamlit as st

# ID của file index.json trên Drive của bạn
MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    filename = "data_index.json"
    url = f'https://drive.google.com/uc?id={MASTER_ID}'
    
    # Xóa file cũ nếu tồn tại để tránh xung đột
    if os.path.exists(filename):
        os.remove(filename)
    
    try:
        gdown.download(url, filename, quiet=False, fuzzy=True)
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Lỗi khi tải file index từ Drive: {e}")
        return {}

def get_lesson_content(file_id):
    output = "lesson.json"
    url = f'https://drive.google.com/uc?id={file_id}'
    
    # Xóa file cũ nếu tồn tại
    if os.path.exists(output):
        os.remove(output)
        
    try:
        gdown.download(url, output, quiet=False, fuzzy=True)
        with open(output, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Lỗi khi tải bài học: {e}")
        return {"vocabulary": []}