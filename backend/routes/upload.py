from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
from gridfs import GridFS
from docling.document_converter import DocumentConverter
import io

router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["resume_db"]
fs = GridFS(db)
parsed_collection = db["parsed_resumes"]

# Initialize DocLing Parser
converter = DocumentConverter()

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    # Step 1: Save file in GridFS
    file_id = fs.put(file.file, filename=file.filename)

    # Step 2: Convert GridFS file to BytesIO for DocLing
    file.file.seek(0)  # Ensure pointer at start
    pdf_bytes = file.file.read()
    pdf_file_like = io.BytesIO(pdf_bytes)

    # Step 3: Parse with DocLing
    try:
        result = converter.convert(pdf_file_like)
        parsed_text = result.document.export_to_markdown()
    except Exception as e:
        return {"message": f"Resume uploaded but parsing failed: {str(e)}"}

    # Step 4: Save parsed text in MongoDB
    parsed_collection.insert_one({
        "resume_file_id": file_id,
        "filename": file.filename,
        "parsed_text": parsed_text
    })

    return {"message": f"Resume uploaded and parsed successfully: {file.filename}"}
