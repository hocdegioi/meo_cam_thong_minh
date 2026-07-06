import gdown
import json
import os
import streamlit as st

# ID của file index.json trên Drive (đã upload dạng tệp tin thô)
MASTER_ID = "1JlFIpJZJ1cgMMlSZo9oCKBv7n3xOljQL" 

def get_master_index():
    filename = "data_index.json"
    url = f'https://drive.google.com/uc?id={MASTER_ID}'
    try:
        gdown.download(url, filename, quiet=False, fuzzy=True)
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Không thể tải file index: {e}")
        return {}

def get_lesson_content(file_id):
    if not file_id or file_id == "...": # Kiểm tra nếu ID chưa có hoặc là "..."
        return {"vocabulary": ["Bài học này chưa có nội dung, bé chọn bài khác nhé!"]}
        gdown.download(url, output, quiet=False, fuzzy=True)
        with open(output, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Không thể tải bài học: {e}")
        return {"vocabulary": []}