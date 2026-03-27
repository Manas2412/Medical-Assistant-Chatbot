from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

from typing import List, Annotated

router=APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files: Annotated[list[UploadFile], File(...)]):
    try:
        logger.info("recieved uploaded file")
        load_vectorstore(files)
        logger.info("Document added to vector store")
        return JSONResponse(status_code=200,content={"message":"Documents uploaded successfully"})

    except Exception as e:
        logger.exception(f"Error uploading PDFs: {e}")
        return JSONResponse(status_code=500,content={"message":"Error uploading PDFs"})