import requests
from config import API_URL

def upload_pdfs_api(files):
    try:
        files_payload=[("files", (f.name, f.read(), "application/pdf")) for f in files]
        # Fixed URL to match server route exactly
        response = requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def ask_question(question):
    try:
        # Send as form data to match FastAPI Form(...) requirement
        response = requests.post(f"{API_URL}/ask/", data={"question": question})
        return response.json()
    except Exception as e:
        return {"error": str(e)}