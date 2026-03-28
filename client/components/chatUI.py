import streamlit as st
from utils.api import ask_question

def render_chat():
    st.subheader("💬 Chat with your Medical Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt:=st.chat_input("Ask a question (e.g., 'What is diabetes?')"):
        st.session_state.messages.append({"role":"user", "content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder=st.empty()
            message_placeholder.markdown("Thinking...")
            response=ask_question(prompt)
            
            # Response contains 'response' and 'sources' from the backend
            if "response" in response:
                answer = response["response"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role":"assistant", "content": answer})
            else:
                error_msg = response.get("error", "Failed to connect to assistant.")
                message_placeholder.error(f"⚠️ {error_msg}")
                st.session_state.messages.append({"role":"assistant", "content": f"⚠️ Error: {error_msg}"})