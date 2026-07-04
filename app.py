import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import drive_manager
import tempfile
import time

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")

# --- Hàm phát âm ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)

# --- Mã JavaScript để lắng nghe liên tục ---
listening_js = """
<script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        // Gửi kết quả về Streamlit
        window.parent.postMessage({type: 'speech', value: transcript}, '*');
    };
    recognition.start();
</script>
"""

# --- Giao diện chính ---
st.title("🐱 Mèo Cam Giao Tiếp")

if 'started' not in st.session_state:
    if st.button("Bấm để bắt đầu giao tiếp với Mèo Cam"):
        st.session_state.started = True
        st.session_state.index = 0
        st.session_state.vocabulary = drive_manager.get_lesson_content("Lop_3", "Unit_1").get('vocabulary', [])
        st.rerun()
else:
    components.html(listening_js, height=0) # Kích hoạt chế độ nghe
    
    idx = st.session_state.index
    vocab = st.session_state.vocabulary
    
    if idx < len(vocab):
        item = vocab[idx]
        word_en = item.get('en', item) if isinstance(item, dict) else str(item)
        word_vi = item.get('vi', '') if isinstance(item, dict) else ''
        
        # Hiển thị bài học
        st.markdown(f"## 🐱 Mèo Cam đang dạy: **{word_en}**")
        st.write(f"### Nghĩa: {word_vi}")
        
        # Mèo Cam đọc (chỉ đọc khi vừa chuyển từ mới)
        if 'last_spoken' not in st.session_state or st.session_state.last_spoken != word_en:
            speak(word_en)
            st.session_state.last_spoken = word_en
        
        # Lắng nghe phản hồi từ JS
        # Lưu ý: Bạn cần dùng st.query_params hoặc callback để nhận postMessage
        # Để đơn giản nhất trong môi trường này, ta giả định cơ chế nhận:
        st.info("🎤 Mèo Cam đang lắng nghe bé...")
        
        # Giả lập logic kiểm tra (Cần thêm cơ chế nhận message từ JS phía trên)
        # Nếu bé nói đúng:
        if st.button("Mô phỏng bé nói đúng (Test)"): 
            st.success("Tuyệt vời! 🌸")
            st.balloons()
            time.sleep(2)
            st.session_state.index += 1
            st.rerun()
            
    else:
        st.write("🎉 Bé đã học xong bài!")