import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import drive_manager
import tempfile
import time

# --- Cấu hình trang ---
st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")
st.title("🐱 Mèo Cam Thông Minh")

# --- Hàm hỗ trợ ---
def speak(text, meaning=None):
    """Phát âm thanh và hiển thị nghĩa tiếng Việt"""
    tts = gTTS(text=text, lang='en')
    # Sử dụng file tạm để không bị ngập file mp3 trong thư mục
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)
    
    display_text = f"### 🐱 Mèo Cam: {text}"
    if meaning:
        display_text += f" <small style='color:gray;'>({meaning})</small>"
    st.write(display_text, unsafe_allow_html=True)

def listen_and_check(target_text):
    """Sử dụng st.audio_input để nhận âm thanh từ trình duyệt"""
    st.info(f"🎤 Bé hãy bấm vào biểu tượng Micro và nói: **{target_text}**")
    
    # Đây là tính năng mới của Streamlit cho phép thu âm trực tiếp trên trình duyệt
    audio_value = st.audio_input("Ghi âm tại đây")
    
    if audio_value:
        st.write("Đang xử lý giọng nói...")
        r = sr.Recognizer()
        try:
            # Đọc dữ liệu từ file âm thanh mà trình duyệt vừa gửi lên
            with sr.AudioFile(audio_value) as source:
                audio = r.record(source)
            
            user_text = r.recognize_google(audio, language="en-US")
            st.write(f"**Bé nói:** *{user_text}*")
            
            if target_text.lower().strip() == user_text.lower().strip():
                st.success("Tuyệt quá! 🌸")
                return True
            else:
                st.warning("Bé thử lại nhé!")
                return False
        except Exception as e:
            st.error("Mèo Cam chưa nghe rõ, bé nói lại nhé!")
            return False

# --- Giao diện chính ---
chon_lop = st.selectbox("Chọn lớp:", ["Lop_3"])
chon_bai = st.text_input("Nhập tên bài:", "Unit_1")

if st.button("Bắt đầu bài học"):
    content = drive_manager.get_lesson_content(chon_lop, chon_bai)
    
    if content and isinstance(content, dict):
        # Lấy danh sách từ vựng, mặc định là danh sách rỗng nếu không thấy
        vocabulary_list = content.get('vocabulary', [])
        
        if not vocabulary_list:
            st.warning("Bài học này chưa có từ vựng nào!")
        
        for item in vocabulary_list:
            # Xử lý thông minh: kiểm tra xem item là từ điển hay chuỗi
            if isinstance(item, dict):
                word_en = item.get('en', '')
                word_vi = item.get('vi', '')
                speak(word_en, word_vi)
                listen_and_check(word_en)
            else:
                # Nếu dữ liệu trong JSON là chuỗi đơn thuần (ví dụ: "Hello")
                speak(str(item))
                listen_and_check(str(item))
    else:
        st.error("Dữ liệu bài học không đúng định dạng. Hãy kiểm tra file JSON trên Drive!")

#