import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import time

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Dạy Bé Học", page_icon="🐱")

# --- Hàm hỗ trợ ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

def process_audio(audio_bytes):
    """Chuyển đổi bytes từ mic_recorder sang văn bản"""
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp_wav:
        with open(tmp_wav.name, "wb") as f:
            f.write(audio_bytes)
        with sr.AudioFile(tmp_wav.name) as source:
            audio = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio, language="en-US").lower()
            except:
                return ""

# --- Khởi tạo Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 'selection' # 'selection' hoặc 'teaching'
    st.session_state.index = 0
    st.session_state.vocab = []

# --- Giao diện chính ---
st.title("🐱 Mèo Cam Giao Tiếp")

if st.session_state.step == 'selection':
    st.subheader("Chọn lớp và bài học để bắt đầu:")
    
    # Giả lập chọn lớp/bài (Bạn có thể thay bằng load từ file JSON/Excel)
    grade = st.selectbox("Chọn lớp:", ["Lớp 3", "Lớp 4", "Lớp 5"])
    lesson = st.selectbox("Chọn bài học:", ["Unit 1", "Unit 2", "Unit 3"])
    
    if st.button("Bắt đầu giao tiếp"):
        # Dữ liệu mẫu (nếu không có file)
        st.session_state.vocab = ["apple", "banana", "cat"] 
        st.session_state.step = 'teaching'
        st.session_state.index = 0
        st.rerun()

elif st.session_state.step == 'teaching':
    idx = st.session_state.index
    
    if idx < len(st.session_state.vocab):
        word = st.session_state.vocab[idx]
        st.subheader(f"Mèo Cam đang dạy: {word}")
        
        # Mèo đọc
        speak(word)
        
        # Ghi âm
        st.write("Bé hãy nhấn vào nút dưới đây và đọc từ vừa rồi nhé:")
        audio = mic_recorder(start_prompt="Đọc ngay!", stop_prompt="Đang kiểm tra...", key='recorder')
        
        if audio:
            user_text = process_audio(audio['bytes'])
            st.write(f"Bé đã nói: {user_text}")
            
            if word.lower() in user_text:
                st.success("Đúng rồi! Tặng bé 1 bông hoa! 🌸")
                time.sleep(1.5)
                st.session_state.index += 1
                st.rerun()
            else:
                st.error("Chưa đúng, thử lại nhé!")
                time.sleep(1)
    else:
        st.balloons()
        st.write("Chúc mừng bé đã hoàn thành bài học!")
        if st.button("Chọn bài khác"):
            st.session_state.step = 'selection'
            st.rerun()