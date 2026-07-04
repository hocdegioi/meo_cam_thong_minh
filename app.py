import streamlit as st
from gtts import gTTS
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import time

st.set_page_config(page_title="Mèo Cam", page_icon="🐱")

def speak(text):
    tts = gTTS(text=text, lang='en')
    with io.BytesIO() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3", autoplay=True)

def process_audio_fast(audio_bytes):
    """Xử lý âm thanh trực tiếp từ bytes, bỏ qua file trung gian"""
    try:
        recognizer = sr.Recognizer()
        # Chuyển bytes thành AudioData trực tiếp nếu có thể, 
        # hoặc dùng AudioFile với BytesIO để giảm thao tác đĩa
        with io.BytesIO(audio_bytes) as audio_file:
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                return recognizer.recognize_google(audio_data, language="en-US").lower()
    except:
        return ""

# --- UI ---
if 'step' not in st.session_state:
    st.session_state.step = 'menu'
    st.session_state.index = 0
    st.session_state.vocab = ["apple", "banana", "cat"]

if st.session_state.step == 'menu':
    if st.button("Bắt đầu bài học"):
        st.session_state.step = 'play'
        st.rerun()
else:
    word = st.session_state.vocab[st.session_state.index]
    st.subheader(f"Mèo Cam: {word}")
    speak(word)
    
    # Nút ghi âm tích hợp sẵn của streamlit-mic-recorder
    audio = mic_recorder(start_prompt="Nhấn vào đây để đọc", stop_prompt="Đang xử lý...", key='mic')
    
    if audio:
        res = process_audio_fast(audio['bytes'])
        if word.lower() in res:
            st.success("Đúng rồi! 🎉")
            time.sleep(1)
            st.session_state.index += 1
            st.rerun()
        else:
            st.error(f"Chưa đúng (Bé nói: {res}). Thử lại nhé!")