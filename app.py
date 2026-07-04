import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

# --- Trạng thái ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocabulary = []

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

# --- Logic chính ---
st.title("🐱 Mèo Cam Giao Tiếp Tự Nhiên")

if st.button("Bắt đầu bài học"):
    content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
    st.session_state.vocabulary = content.get('vocabulary', [])
    st.session_state.index = 0

if st.session_state.vocabulary:
    idx = st.session_state.index
    if idx < len(st.session_state.vocabulary):
        item = st.session_state.vocabulary[idx]
        word_en = item.get('en', item) if isinstance(item, dict) else str(item)
        word_vi = item.get('vi', '') if isinstance(item, dict) else ''
        
        # Mèo Cam đọc
        st.markdown(f"## 🐱 Mèo Cam: **{word_en}** <small>({word_vi})</small>", unsafe_allow_html=True)
        speak(word_en)
        
        # Ghi âm tự động
        st.write("🎤 Mèo Cam đang nghe bé đọc...")
        audio = mic_recorder(start_prompt="Bé nói đi", stop_prompt="Đang xử lý...", key=f"mic_{idx}")
        
        if audio:
            # Ở đây bạn thêm hàm chuyển giọng nói thành text (Speech-to-Text)
            # Nếu bé nói đúng:
            st.success("Tuyệt vời! 🌸")
            st.balloons()
            st.session_state.index += 1
            st.rerun()
    else:
        st.write("🎉 Bé đã hoàn thành bài!")