import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager
import speech_recognition as sr
from pydub import AudioSegment
import time

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")
st.title("🐱 Mèo Cam Giao Tiếp Tự Nhiên")

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

def check_audio(audio_bytes, target_word):
    """Chuyển đổi âm thanh và kiểm tra đúng sai"""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".webm") as tmp_webm:
        tmp_webm.write(audio_bytes)
        tmp_webm.flush()
        audio_converted = AudioSegment.from_file(tmp_webm.name, format="webm")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp_wav:
            audio_converted.export(tmp_wav.name, format="wav")
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_wav.name) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="en-US")
                    return text.lower().strip() == target_word.lower().strip()
                except:
                    return False

# --- Logic giao diện ---
if not st.session_state.started:
    if st.button("Bắt đầu bài học"):
        content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
        st.session_state.vocabulary = content.get('vocabulary', [])
        st.session_state.index = 0
        st.session_state.started = True
        st.rerun()

if st.session_state.started and st.session_state.vocabulary:
    idx = st.session_state.index
    if idx < len(st.session_state.vocabulary):
        item = st.session_state.vocabulary[idx]
        word_en = item.get('en', item) if isinstance(item, dict) else str(item)
        word_vi = item.get('vi', '') if isinstance(item, dict) else ''
        
        # Hiển thị từ
        st.markdown(f"## 🐱 Mèo Cam: **{word_en}** <small>({word_vi})</small>", unsafe_allow_html=True)
        speak(word_en)
        
        # Ghi âm với KEY ĐỘNG (xử lý lỗi DuplicateElementId)
        audio = mic_recorder(
            start_prompt="Bấm để nói", 
            stop_prompt="Đang lắng nghe...", 
            key=f"mic_{idx}"
        )
        
        if audio:
            st.write("Đang kiểm tra...")
            if check_audio(audio['bytes'], word_en):
                st.success("🌸 Tuyệt vời! Bé nói đúng rồi!")
                st.balloons()
                time.sleep(1)
                st.session_state.index += 1
                st.rerun()
            else:
                st.warning("Mèo Cam chưa nghe rõ, bé đọc lại nhé!")
    else:
        st.success("🎉 Bé đã hoàn thành bài học!")
        if st.button("Học bài mới"):
            st.session_state.started = False
            st.rerun()