import streamlit as st
from components.upload import render_upload
from components.chatUI import render_chat
from components.history_download import render_history_download

st.set_page_config(
    page_title="Medical Assistant Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for Upload and History
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
    st.title("MediBot Control Panel")
    render_upload()
    st.divider()
    render_history_download()

# Main Chat Interface
st.title("👨‍⚕️ Medical Assistant Chatbot")
st.caption("🚀 AI-powered RAG Medical assistant to help you understand your medical reports.")

render_chat()