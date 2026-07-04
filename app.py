import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

# --- Trạng thái lưu bài học ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocabulary = []

def speak(text):
    """Phát âm thanh bằng gTTS"""
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

# --- Giao diện chính ---
st.title("🐱 Mèo Cam Giao Tiếp Tự Nhiên")

if st.button("Bắt đầu bài học"):
    content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
    if content:
        st.session_state.vocabulary = content.get('vocabulary', [])
        st.session_state.index = 0
        st.rerun()

# --- Luồng học từng từ ---
if st.session_state.vocabulary:
    idx = st.session_state.index
    if idx < len(st.session_state.vocabulary):
        item = st.session_state.vocabulary[idx]
        word_en = item.get('en', item) if isinstance(item, dict) else str(item)
        word_vi = item.get('vi', '') if isinstance(item, dict) else ''
        
        # 1. Mèo Cam dạy
        st.markdown(f"## 🐱 Mèo Cam: **{word_en}** <small>({word_vi})</small>", unsafe_allow_html=True)
        speak(word_en)
        
        # 2. Ghi âm rảnh tay (Sử dụng key động để tránh lỗi DuplicateElementId)
        st.write("🎤 Mèo Cam đang nghe bé đọc...")
        audio = mic_recorder(
            start_prompt="Bấm để nói", 
            stop_prompt="Đang xử lý...", 
            key=f"mic_{idx}"
        )
        
        if audio:
            # Logic kiểm tra giọng nói (Bạn có thể thêm Speech-to-Text tại đây)
            st.success("Tuyệt vời! 🌸")
            st.balloons()
            st.session_state.index += 1
            st.rerun()
    else:
        st.write("🎉 Chúc mừng bé đã hoàn thành bài học!")
        if st.button("Học lại từ đầu"):
            st.session_state.index = 0
            st.rerun()