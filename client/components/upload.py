import streamlit as st
from utils.api import upload_pdfs_api

def render_upload():
    st.subheader("📁 Upload Medical PDFs")

    uploaded_files=st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True, key="pdf_uploader")

    if st.button("🚀 Start Processing"):
        if uploaded_files:
            with st.spinner("Processing & Indexing..."):
                response=upload_pdfs_api(uploaded_files)
                if response.get("message"):
                    st.success(response.get("message"))
                elif response.get("error"):
                    st.error(f"Error: {response.get('error')}")
                else:
                    st.warning("No message received from server.")
        else:
            st.warning("Please select PDF files to upload")