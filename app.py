import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import tempfile
import time

# --- Hàm phát âm ---
def speak_and_show(text, meaning):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3", autoplay=True)
    st.markdown(f"## 🐱 Mèo Cam: {text} <span style='font-size:20px; color:gray;'>({meaning})</span>", unsafe_allow_html=True)

# --- Component xử lý giọng nói liên tục (Web Speech API) ---
# Đoạn mã này sẽ tự động gửi kết quả từ trình duyệt về Streamlit
speech_js = """
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

st.title("🐱 Mèo Cam Giao Tiếp Tự Nhiên")

if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.vocabulary = [{"en": "Hello", "vi": "Xin chào"}, {"en": "Cat", "vi": "Con mèo"}]

# Kích hoạt chế độ nghe
components.html(speech_js, height=0)

# Hiển thị từ hiện tại
idx = st.session_state.index
if idx < len(st.session_state.vocabulary):
    item = st.session_state.vocabulary[idx]
    word_en = item['en']
    word_vi = item['vi']
    
    speak_and_show(word_en, word_vi)
    st.info("🎤 Mèo Cam đang nghe bé đọc...")

    # Nhận kết quả từ JS
    # Trong Streamlit, để nhận tin nhắn từ JS, ta thường dùng st.chat_input hoặc 
    # query_params. Ở đây ta sử dụng một cơ chế logic đơn giản:
    # Bé đọc xong, ứng dụng tự so sánh:
    
    user_input = st.text_input("Bé đọc vào đây (Mô phỏng giọng nói):") # Dùng thay thế cho JS tạm thời
    
    if user_input:
        if user_input.lower().strip() == word_en.lower().strip():
            st.success("🌸 Tuyệt vời! Bé nói đúng rồi!")
            st.balloons()
            time.sleep(2)
            st.session_state.index += 1
            st.rerun()
        else:
            st.warning("Bé đọc lại nhé, chưa đúng rồi!")
else:
    st.write("🎉 Bé đã hoàn thành bài!")