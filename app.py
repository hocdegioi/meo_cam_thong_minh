import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager
import speech_recognition as sr
from pydub import AudioSegment
import time

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

# --- Hàm phát âm ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

# --- Hàm kiểm tra nhanh ---
def check_audio_fast(audio_bytes, target_word):
    # Sử dụng recognizer nhanh hơn
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False # Bỏ qua bước đo mức âm thanh
    recognizer.energy_threshold = 300 
    
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".webm") as tmp_webm:
            tmp_webm.write(audio_bytes)
            tmp_webm.flush()
            audio_converted = AudioSegment.from_file(tmp_webm.name, format="webm")
            
            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp_wav:
                audio_converted.export(tmp_wav.name, format="wav", codec="pcm_s16le")
                with sr.AudioFile(tmp_wav.name) as source:
                    audio_data = recognizer.record(source)
                    # Timeout cực ngắn để phản hồi ngay
                    text = recognizer.recognize_google(audio_data, language="en-US")
                    return text.lower().strip() == target_word.lower().strip()
    except:
        return False

# --- Logic chính ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.started = False

st.title("🐱 Mèo Cam Giao Tiếp Tốc Độ")

if not st.session_state.started:
    if st.button("Bắt đầu ngay"):
        content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
        st.session_state.vocabulary = content.get('vocabulary', [])
        st.session_state.started = True
        st.rerun()

if st.session_state.started:
    vocab = st.session_state.vocabulary
    idx = st.session_state.index
    
    if idx < len(vocab):
        item = vocab[idx]
        word = item.get('en', item) if isinstance(item, dict) else str(item)
        
        st.subheader(f"Mèo Cam nói: {word}")
        
        # Ghi âm tốc độ cao
        audio = mic_recorder(start_prompt="Nói ngay!", stop_prompt="Đang check...", key=f"fast_{idx}")
        
        if audio:
            with st.spinner('Mèo Cam đang kiểm tra...'):
                if check_audio_fast(audio['bytes'], word):
                    st.success("Đúng rồi! 🎉")
                    st.balloons()
                    time.sleep(0.5) # Giảm thời gian chờ
                    st.session_state.index += 1
                    st.rerun()
                else:
                    st.error("Chưa đúng, đọc lại đi bé!")
                    time.sleep(1)
                    st.rerun()
    else:
        st.write("Hoàn thành bài!")
        if st.button("Chọn bài khác"):
            st.session_state.started = False
            st.rerun()