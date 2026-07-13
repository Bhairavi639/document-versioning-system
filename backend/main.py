from fastapi import FastAPI, UploadFile, File
import shutil
import os

from services.compare_service import compare_excel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from services.report_service import (
    generate_docx_report,
    generate_csv_report
)
from fastapi.responses import FileResponse
from utils.pdf_reader import read_pdf
from utils.doc_reader import read_docx  # assuming you already have this

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running"}


# ✅ Upload API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


# ✅ Compare API (basic text compare)
@app.post("/download/csv")
async def download_csv(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    # Save uploaded files
    with open(file1_path, "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open(file2_path, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    
    # Compare Excel files directly
    diff_result = compare_excel(
        file1_path,
        file2_path
    )
    report_path = generate_docx_report(
        diff_result,
        file1.filename,
        file2.filename
    )

    # Generate CSV
    csv_path = generate_csv_report(diff_result)

    return FileResponse(
        path=csv_path,
        filename="comparison_report.csv",
        media_type="text/csv"
    )


from models.response_model import CompareResponse  # ADD THIS

@app.post("/compare")
async def compare(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    file1_path = os.path.join("uploads", file1.filename)
    file2_path = os.path.join("uploads", file2.filename)

    os.makedirs("uploads", exist_ok=True)

    with open(file1_path, "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open(file2_path, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    ext = os.path.splitext(file1.filename)[1].lower()

    # ==========================
    # EXCEL COMPARISON
    # ==========================
    if ext == ".xlsx":

        diff_result = compare_excel(
            file1_path,
            file2_path
        )
        
    # ==========================
    # PDF / DOCX COMPARISON
    # ==========================
    else:

        text1 = extract_text(file1_path)
        text2 = extract_text(file2_path)

        diff_result = compare_excel(
            text1,
            text2
        )

    report_path = generate_docx_report(
        diff_result,
        file1.filename,
        file2.filename
    )

    return {
        "file1": file1.filename,
        "file2": file2.filename,
        "diff": diff_result,
        "report_path": report_path
    }


@app.get("/download-report")
def download_report(path: str):
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(path)
    )

def extract_text(file_path):
    """
    Detect file type and extract text accordingly
    """

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return read_pdf(file_path)

    elif ext == ".docx":
        return read_docx(file_path)

    else:
        raise ValueError("Unsupported file format")