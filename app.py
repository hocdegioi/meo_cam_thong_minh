import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager
import speech_recognition as sr # Thêm thư viện nhận diện giọng nói

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocabulary = []

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

# Hàm kiểm tra giọng nói
def check_audio(audio_bytes, target_word):
    recognizer = sr.Recognizer()
    # Chuyển audio_bytes thành file tạm để recognizer xử lý
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav.write(audio_bytes)
        tmp_wav_path = tmp_wav.name
    
    with sr.AudioFile(tmp_wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Nhận diện giọng nói bằng Google Speech Recognition
            text = recognizer.recognize_google(audio_data, language="en-US")
            return text.lower() == target_word.lower()
        except:
            return False

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
        
        st.markdown(f"## 🐱 Mèo Cam: **{word_en}** <small>({word_vi})</small>", unsafe_allow_html=True)
        speak(word_en)
        
        audio = mic_recorder(start_prompt="Bé nói đi", stop_prompt="Đang lắng nghe...", key=f"mic_{idx}")
        
        if audio:
            st.write("Đang kiểm tra giọng nói...")
            is_correct = check_audio(audio['bytes'], word_en)
            if is_correct:
                st.success("🌸 Tuyệt vời! Bé nói đúng rồi!")
                st.balloons()
                st.session_state.index += 1
                st.rerun()
            else:
                st.warning("Bé thử đọc lại nhé!")
    else:
        st.write("🎉 Bé đã hoàn thành bài!")