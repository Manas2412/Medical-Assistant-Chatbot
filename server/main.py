from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_pdf_router
from routes.ask_question import router as ask_question_router

app = FastAPI(title="Medical Assistant API", description="API for AI Medical Assistant ChatBot")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# middleware exception handler
app.middleware("http")(catch_exception_middleware)

# routers
# 1. upload pdfs documents
app.include_router(upload_pdf_router)
# 2. asking query
app.include_router(ask_question_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)