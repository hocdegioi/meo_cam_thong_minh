import gdown
import json
import os
import streamlit as st

# ID file index.json của bạn trên Drive
MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    filename = "data_index.json"
    url = f'https://drive.google.com/uc?id={MASTER_ID}'
    
    try:
        if os.path.exists(filename):
            os.remove(filename)
            
        # Bỏ tham số fuzzy=True để không bị lỗi
        gdown.download(url, filename, quiet=False)
        
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Lỗi tải file index: {e}")
        return {}

def get_lesson_content(file_id):
    output = "lesson.json"
    url = f'https://drive.google.com/uc?id={file_id}'
    
    try:
        if os.path.exists(output):
            os.remove(output)
            
        # Bỏ tham số fuzzy=True để không bị lỗi
        gdown.download(url, output, quiet=False)
        
        with open(output, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Lỗi tải bài học: {e}")
        return {"vocabulary": []}