import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
import time
import drive_manager # Giả định bạn đã có module này trong thư mục dự án

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Dạy Bé Học", page_icon="🐱")

# --- Hàm hỗ trợ ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

def listen_to_child():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # Thời gian chờ bé đọc là 3 giây
        audio = recognizer.listen(source, phrase_time_limit=3)
    try:
        return recognizer.recognize_google(audio, language="en-US").lower()
    except:
        return ""

# --- Khởi tạo trạng thái an toàn ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocab = [] # Khởi tạo danh sách trống để tránh lỗi
    st.session_state.started = False

st.title("🐱 Mèo Cam Giao Tiếp")

# --- Luồng xử lý ---
if not st.session_state.started:
    if st.button("Bắt đầu bài học"):
        # Lấy dữ liệu từ hệ thống của bạn[cite: 1]
        content = drive_manager.get_lesson_content("Lop_3", "Unit_1")
        st.session_state.vocab = content.get('vocabulary', ["apple", "banana", "cat"]) 
        st.session_state.started = True
        st.rerun()
else:
    # Chỉ thực hiện khi vocab đã được khởi tạo
    if st.session_state.index < len(st.session_state.vocab):
        idx = st.session_state.index
        target_word = st.session_state.vocab[idx]
        
        st.subheader(f"Mèo Cam nói: {target_word}")
        
        # 1. Mèo dạy
        speak(target_word)
        
        # 2. Tự động lắng nghe
        st.info("Mèo Cam đang đợi bé đọc...")
        user_said = listen_to_child()
        
        # 3. Phản hồi
        if user_said:
            st.write(f"Bé vừa nói: {user_said}")
            if target_word.lower() in user_said:
                st.success("Đúng rồi! Tặng bé 1 bông hoa! 🌸")
                time.sleep(1.5)
                st.session_state.index += 1
                st.rerun()
            else:
                st.error("Chưa đúng, Mèo đọc lại nhé!")
                time.sleep(1)
    else:
        st.balloons()
        st.write("Chúc mừng bé đã hoàn thành bài học!")
        if st.button("Học lại từ đầu"):
            st.session_state.index = 0
            st.rerun()