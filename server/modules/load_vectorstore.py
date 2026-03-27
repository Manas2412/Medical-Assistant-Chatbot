import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV='us-east-1'
PINECONE_INDEX_NAME="medical-index"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


UPLOAD_DIR="./upload_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


# initialize pinecone instance
pc=Pinecone(api_key=PINECONE_API_KEY)
# ServerlessSpec is used in create_index
existing_indexes=[i.name for i in pc.list_indexes().indexes]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)

index=pc.Index(PINECONE_INDEX_NAME)


# load, split, embed and upsert pdf docs content

def load_vectorstore(uploaded_files):
    embed_model=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_path=[]

    # 1. upload
    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        file_path.append(str(save_path))

    # 2. splitting
    for file_path in file_path:
        loader=PyPDFLoader(file_path)
        docs=loader.load()

        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n","\n"," ",""]
        )

        split_docs=text_splitter.split_documents(docs)
        
        texts=[chunk.page_content for chunk in split_docs]
        metadatas=[chunk.metadata for chunk in split_docs]
        ids=[str(uuid.uuid4()) for _ in range(len(split_docs))]

        # 3. embedding
        print(f"Embidding chunks")
        embedding=embed_model.embed_documents(texts)

        # 4. upsert
        print(f"Upserting into Pinecone")
        with tqdm(total=len(embedding),desc="Upserting to Pinecone") as progress_bar:
            for i in range(0,len(embedding),32):
                batch_embedding=embedding[i:i+32]
                batch_metadata=metadatas[i:i+32]
                batch_ids=ids[i:i+32]
                index.upsert(vectors=zip(batch_ids,batch_embedding,batch_metadata))
                progress_bar.update(32)

        print(f"Upserted {len(embedding)} vectors")

        
        