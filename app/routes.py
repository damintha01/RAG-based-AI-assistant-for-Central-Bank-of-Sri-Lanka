from fastapi import APIRouter, UploadFile, File
from app.schemas import AskRequest, AskResponse
from retriever.rag_pipeline import ask
import shutil
import os

router = APIRouter()

# =============================
# POST /ask
# =============================
@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    result = ask(request.question)

    return result


# =============================
# POST /upload
# =============================
@router.post("/upload")
def upload_document(file: UploadFile = File(...)):

    upload_path = f"data/raw/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"{file.filename} uploaded successfully."}


# =============================
# GET /documents
# =============================
@router.get("/documents")
def list_documents():

    processed_path = "data/processed/"
    documents = [
        f.replace(".json", "")
        for f in os.listdir(processed_path)
        if f.endswith(".json")
    ]

    return {"documents": documents}