import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager
import time

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

# --- Trạng thái ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocabulary = []
    st.session_state.started = False

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

st.title("🐱 Mèo Cam Giao Tiếp Tự Nhiên")

# 1. Nút bấm duy nhất để kích hoạt quyền Micro
if not st.session_state.started:
    if st.button("Bấm vào đây để Mèo Cam bắt đầu dạy"):
        content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
        st.session_state.vocabulary = content.get('vocabulary', [])
        st.session_state.index = 0
        st.session_state.started = True
        st.rerun()

# 2. Vòng lặp học tập tự động
if st.session_state.started and st.session_state.vocabulary:
    idx = st.session_state.index
    
    if idx < len(st.session_state.vocabulary):
        item = st.session_state.vocabulary[idx]
        word_en = item.get('en', item) if isinstance(item, dict) else str(item)
        word_vi = item.get('vi', '') if isinstance(item, dict) else ''
        
        # Mèo Cam dạy
        st.markdown(f"## 🐱 Mèo Cam: **{word_en}** <small>({word_vi})</small>", unsafe_allow_html=True)
        speak(word_en)
        
        # Mèo Cam chờ bé đọc (Chỉ hiện nút micro 1 lần cho từ đó)
        st.info("🎤 Bé hãy đọc theo Mèo Cam nhé...")
        audio = mic_recorder(start_prompt="Bấm vào đây để Mèo Cam nghe", stop_prompt="Đang lắng nghe...", key=f"mic_{idx}")
        
        if audio:
            # Kiểm tra giọng nói (Giả lập logic đúng/sai)
            # Ở đây bạn có thể tích hợp API Speech-to-Text của Google
            st.success("🌸 Tuyệt vời! Bé nói đúng rồi!")
            st.balloons()
            time.sleep(2) # Khen xong chờ 2 giây rồi qua từ mới
            st.session_state.index += 1
            st.rerun()
    else:
        st.success("🎉 Chúc mừng bé đã hoàn thành bài học!")
        if st.button("Trở về màn hình chính"):
            st.session_state.started = False
            st.rerun()