import os
import requests

# ---------------- CONFIG ----------------
FOLDER_PATH = "TechResume"  # <-- Change this
API_URL = "http://127.0.0.1:8000/upload/"  # Your FastAPI upload endpoint
# ----------------------------------------

def upload_pdf(file_path):
    """Upload a single PDF to the FastAPI backend."""
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        response = requests.post(API_URL, files=files)
    if response.status_code == 200:
        print(f"✅ Uploaded: {os.path.basename(file_path)}")
    else:
        print(f"❌ Failed: {os.path.basename(file_path)} -> {response.status_code}")

def upload_folder(folder_path):
    """Iterate through all PDFs in folder and upload them."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                upload_pdf(file_path)

if __name__ == "__main__":
    upload_folder(FOLDER_PATH)
