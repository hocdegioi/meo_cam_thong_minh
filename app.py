import streamlit as st
from gtts import gTTS
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import time

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Dạy Bé Học", page_icon="🐱")

# --- Hàm xử lý âm thanh ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    with io.BytesIO() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3", autoplay=True)

def process_audio(audio_bytes):
    try:
        # Chuyển đổi âm thanh trình duyệt sang WAV chuẩn bằng pydub
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data, language="en-US").lower()
    except Exception as e:
        return ""

# --- Khởi tạo trạng thái ---
if 'step' not in st.session_state:
    st.session_state.step = 'selection'
    st.session_state.index = 0
    st.session_state.vocab = []

# --- Logic Giao diện ---
st.title("🐱 Mèo Cam Giao Tiếp")

if st.session_state.step == 'selection':
    st.subheader("Chọn lớp và bài học:")
    grade = st.selectbox("Lớp:", ["Lớp 3", "Lớp 4", "Lớp 5"])
    lesson = st.selectbox("Bài học:", ["Unit 1", "Unit 2", "Unit 3"])
    
    if st.button("Bắt đầu bài học"):
        # Ở đây bạn có thể nạp dữ liệu thật từ drive_manager
        st.session_state.vocab = ["apple", "banana", "cat"] 
        st.session_state.step = 'teaching'
        st.session_state.index = 0
        st.rerun()

elif st.session_state.step == 'teaching':
    idx = st.session_state.index
    if idx < len(st.session_state.vocab):
        word = st.session_state.vocab[idx]
        st.subheader(f"Mèo Cam đang dạy từ: **{word}**")
        
        # Mèo nói
        speak(word)
        
        # Bé đọc (Nút bấm của mic_recorder)
        audio = mic_recorder(start_prompt="Nhấn để đọc từ này", stop_prompt="Đang kiểm tra...", key='recorder')
        
        if audio:
            user_text = process_audio(audio['bytes'])
            if word.lower() in user_text:
                st.success(f"Tuyệt vời! Bé đã nói đúng: {user_text} 🌸")
                time.sleep(1.5)
                st.session_state.index += 1
                st.rerun()
            else:
                st.error(f"Chưa đúng, bé nói là '{user_text}'. Thử lại nhé!")
    else:
        st.balloons()
        st.write("Chúc mừng bé đã hoàn thành bài học!")
        if st.button("Chọn bài mới"):
            st.session_state.step = 'selection'
            st.rerun()