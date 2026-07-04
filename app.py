import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import time

# --- Cấu hình ---
st.set_page_config(page_title="Mèo Cam Học Tiếng Anh", page_icon="🐱")

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    st.audio("temp.mp3", format="audio/mp3", autoplay=True)

def listen_fast():
    """Lắng nghe trực tiếp từ micro máy tính - Phản hồi cực nhanh"""
    r = sr.Recognizer()
    # Cấu hình để nhận diện nhanh, không chờ đợi lâu
    r.pause_threshold = 0.8 
    with sr.Microphone() as source:
        st.write("🎤 Mèo Cam đang nghe...")
        audio = r.listen(source, phrase_time_limit=3)
    try:
        return r.recognize_google(audio, language="en-US").lower()
    except:
        return ""

# --- Trạng thái ---
if 'step' not in st.session_state:
    st.session_state.step = 'menu'
    st.session_state.index = 0
    st.session_state.vocab = []

st.title("🐱 Mèo Cam Giao Tiếp")

if st.session_state.step == 'menu':
    grade = st.selectbox("Chọn lớp:", ["Lớp 3", "Lớp 4", "Lớp 5"])
    if st.button("Bắt đầu bài học"):
        st.session_state.vocab = ["apple", "banana", "cat"] # Nạp dữ liệu từ file của bạn
        st.session_state.step = 'play'
        st.rerun()

elif st.session_state.step == 'play':
    idx = st.session_state.index
    if idx < len(st.session_state.vocab):
        word = st.session_state.vocab[idx]
        st.subheader(f"Mèo Cam: {word}")
        
        # Mèo phát âm
        speak(word)
        
        # Bé nói (Không cần bấm nút, tự động lắng nghe)
        user_said = listen_fast()
        
        if user_said:
            st.write(f"Bé đã nói: {user_said}")
            if word in user_said:
                st.success("Đúng rồi! 🎉")
                time.sleep(1)
                st.session_state.index += 1
                st.rerun()
            else:
                st.error("Chưa đúng, thử lại nhé!")