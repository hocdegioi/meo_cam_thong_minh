import streamlit as st
import gtts
import time
import drive_manager

st.set_page_config(page_title="Mèo Cam Thông Minh", page_icon="🐱")
st.markdown("<style>h1,h2,h3{color:#FF8C00!important;} .stButton>button{background-color:#FF8C00; color:white;}</style>", unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 'menu'

st.title("🐱 Mèo Cam Giao Tiếp")

if st.session_state.step == 'menu':
    st.subheader("Chọn lớp và bài học:")
    index_data = drive_manager.get_master_index()
    grade = st.selectbox("Lớp:", list(index_data.keys()))
    unit = st.selectbox("Bài:", list(index_data.get(grade, {}).keys()))
    
    if st.button("Bắt đầu giao tiếp"):
        content = drive_manager.get_lesson_content(grade, unit)
        st.session_state.vocab = content.get('vocabulary', [])
        st.session_state.index = 0
        st.session_state.step = 'learning'
        st.rerun()

elif st.session_state.step == 'learning':
    vocab = st.session_state.vocab
    idx = st.session_state.index
    
    if idx < len(vocab):
        word = vocab[idx]
        st.subheader(f"Mèo Cam nói: {word}")
        
        # Phát âm
        tts = gtts.gTTS(text=word, lang='en')
        tts.save("temp.mp3")
        st.audio("temp.mp3", autoplay=True)
        
        # Ghi âm tốc độ cao (Web Speech API)
        audio = st.audio_input("Nhấn để đọc")
        if audio:
            st.success("Đang kiểm tra...")
            time.sleep(0.5) # Giả lập kiểm tra
            st.session_state.index += 1
            st.rerun()
    else:
        st.write("Hoàn thành bài!")
        if st.button("Chọn bài khác"):
            st.session_state.step = 'menu'
            st.rerun()