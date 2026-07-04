import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile
import drive_manager
import speech_recognition as sr
from pydub import AudioSegment # Nhập thêm thư viện này

# --- Hàm kiểm tra giọng nói đã sửa ---
def check_audio(audio_bytes, target_word):
    # 1. Lưu bytes tạm thời để pydub đọc
    with tempfile.NamedTemporaryFile(delete=True, suffix=".webm") as tmp_webm:
        tmp_webm.write(audio_bytes)
        tmp_webm.flush()
        
        # 2. Chuyển đổi WebM sang WAV bằng pydub
        audio_converted = AudioSegment.from_file(tmp_webm.name, format="webm")
        
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp_wav:
            audio_converted.export(tmp_wav.name, format="wav")
            
            # 3. Sử dụng SpeechRecognition đọc file WAV đã chuyển
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_wav.name) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="en-US")
                    return text.lower().strip() == target_word.lower().strip()
                except:
                    return False

# --- Phần logic chính trong app.py giữ nguyên ---
# ... (Phần hiển thị của bạn)
        if audio:
            st.write("Đang kiểm tra giọng nói...")
            is_correct = check_audio(audio['bytes'], word_en) # Giờ đã đọc được rồi!
            if is_correct:
                st.success("🌸 Tuyệt vời! Bé nói đúng rồi!")
                st.balloons()
                st.session_state.index += 1
                st.rerun()
            else:
                st.warning(f"Mèo Cam chưa nghe rõ, bé thử đọc lại nhé!")