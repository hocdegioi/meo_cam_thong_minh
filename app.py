import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
import time
import os

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Dạy Bé Học", page_icon="🐱")

# --- Hàm hỗ trợ ---
def speak(text):
    """Mèo Cam phát âm từ vựng"""
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

def listen_to_child():
    """Lắng nghe giọng bé mà không cần nhấn nút"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=3)
    try:
        return recognizer.recognize_google(audio, language="en-US").lower()
    except:
        return ""

# --- Khởi tạo trạng thái ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocab = ["apple", "banana", "cat"] # Mẫu, bạn thay bằng data_loader
    st.session_state.started = False

st.title("🐱 Mèo Cam Học Tiếng Anh")

# --- Giao diện ---
if not st.session_state.started:
    if st.button("Bắt đầu bài học (Nhấn 1 lần duy nhất)"):
        st.session_state.started = True
        st.rerun()
else:
    idx = st.session_state.index
    if idx < len(st.session_state.vocab):
        target_word = st.session_state.vocab[idx]
        
        st.subheader(f"Mèo Cam đang dạy: {target_word}")
        st.image("images/meo_cam.gif") # Bạn nhớ để file gif trong thư mục images
        
        # 1. Mèo dạy
        speak(target_word)
        st.write("Mèo Cam: Bé đọc lại đi nào...")
        
        # 2. Tự động lắng nghe
        user_said = listen_to_child()
        
        # 3. Phản hồi
        if user_said:
            st.write(f"Bé đã nói: {user_said}")
            if target_word in user_said:
                st.success("Đúng rồi! Tặng bé một bông hoa! 🌸")
                time.sleep(2)
                st.session_state.index += 1
                st.rerun()
            else:
                st.error("Chưa đúng, thử lại nhé!")
                time.sleep(1)
    else:
        st.balloons()
        st.write("Chúc mừng bé đã hoàn thành bài học!")