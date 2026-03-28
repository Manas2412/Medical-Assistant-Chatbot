# 👨‍⚕️ Medical Assistant Chatbot (MediBot)

A production-ready RAG (Retrieval-Augmented Generation) Healthcare Assistant that allows users to seamlessly upload medical reports (PDFs) and ask contextual questions. Uses **FastAPI** for a robust backend and **Streamlit** for a modern, interactive frontend. 

## 🚀 Key Features
* 📁 **PDF Ingestion:** Upload multiple PDFs dynamically.
* 🧠 **Smart RAG Pipeline:** Contextually aware document embedding using Google Gemini Embeddings and Pinecone vector database.
* 💬 **Local LLM Integration:** Uses `llama3.1` running securely on your local device via **Ollama**.
* 💾 **History Management:** Export and easily download your chat logs as a `.txt` file for personal record-keeping.

---

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python, Uvicorn 
* **Frontend:** Streamlit, Requests 
* **LLM Orchestration:** LangChain
* **Embeddings:** Google Generative AI (`models/gemini-embedding-2-preview`)
* **Vector Database:** Pinecone
* **Package Management:** `uv`

---

## ⚙️ Prerequisites
1. **Ollama**: Ensure you have [Ollama installed](https://ollama.com/) and running locally.
   ```bash
   ollama run llama3.1
   ```
2. **Pinecone**: You will need a Pinecone account and API key for the vector storage.
3. **Google API Key**: For generating fast and high-quality document embeddings.
4. **`uv` Package Manager**: Ensure `uv` is installed globally.

---

## 🔑 Environment Variables
Create a `.env` file in the `server` directory and add the following keys:
```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medical-index
```

---

## 🏃‍♂️ How to Run the App

The project is split into two directories: `server` and `client`. You need to run both concurrently in separate terminal windows.

### 1. Start the Backend (FastAPI)
Navigate to the server folder and run the FastAPI app:
```bash
cd server
uv sync
uv run main.py
```
*The server will start at `http://0.0.0.0:8000` with hot-reloading enabled.*

### 2. Start the Frontend (Streamlit)
Open a new terminal, navigate to the client folder, and launch Streamlit:
```bash
cd client
uv run streamlit run app.py
```
*Your browser will automatically open the UI at `http://localhost:8501`.*

---

## 📖 Usage
1. Open the **MediBot Control Panel** in your browser sidebar.
2. Drag and drop any specific medical or technical PDF documents.
3. Click **Start Processing** to embed and vectorize the documents into Pinecone.
4. Use the main chat window to ask detailed medical questions (e.g., *"What is diabetes?"* or *"What are my blood test results?"*). The assistant will answer using the provided document context without hallucinating facts.

---

*Note: This chatbot is intended for educational and assistant usage. Always consult a certified healthcare professional regarding medical decisions.*
