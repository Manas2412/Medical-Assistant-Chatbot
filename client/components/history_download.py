import streamlit as st

def render_history_download():
    # Ensure messages exist in session state and there is at least one message
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        # Create a formatted string of the chat history
        chat_text = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state["messages"]])
        
        st.download_button(
            label="💾 Download Chat History",
            data=chat_text,
            file_name="medical_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )