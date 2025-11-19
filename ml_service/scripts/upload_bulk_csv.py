import os
import requests
import pandas as pd

# ---------------- CONFIG ----------------
CSV_PATH = "data.csv"                                # CSV file
API_URL = "http://127.0.0.1:8000/upload/"            # FastAPI upload endpoint
TEMP_DIR = "temp_resumes"                            # Temp folder for PDFs
# ----------------------------------------

os.makedirs(TEMP_DIR, exist_ok=True)


def download_pdf(pdf_url, roll_no):
    """Download a PDF from URL and save it locally."""
    try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to download (Roll: {roll_no}): {e}")
        return None

    file_path = os.path.join(TEMP_DIR, f"{roll_no}.pdf")

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


def upload_pdf(file_path, roll_no):
    """Upload a single PDF to FastAPI backend."""
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            response = requests.post(API_URL, files=files)
    except Exception as e:
        print(f"❌ Upload failed for Roll {roll_no}: {e}")
        return False

    if response.status_code == 200:
        print(f"✅ Uploaded Roll No: {roll_no}")
        return True
    else:
        print(f"❌ Upload API error for Roll {roll_no}: {response.status_code}")
        return False


def process_csv(csv_path):
    """Read CSV, filter unique roll numbers, download & upload PDFs."""
    df = pd.read_csv(csv_path)

    # ----------------------------
    # 🔥 Remove duplicates by Roll Number
    # keeps the first occurrence only
    df_unique = df.drop_duplicates(subset=["Student Roll No"], keep="first")
    # ----------------------------

    print(f"📌 Total rows in CSV       : {len(df)}")
    print(f"📌 Unique Roll Numbers    : {len(df_unique)}")
    print("--------------------------------------------------")

    for _, row in df_unique.iterrows():
        roll_no = row["Student Roll No"]
        pdf_url = row["Resume Link"]

        print(f"📄 Processing Roll No: {roll_no}")

        # 1. Download PDF
        local_pdf = download_pdf(pdf_url, roll_no)
        if not local_pdf:
            continue

        # 2. Upload PDF
        upload_pdf(local_pdf, roll_no)

        # 3. Delete temp file
        os.remove(local_pdf)


if __name__ == "__main__":
    process_csv(CSV_PATH)
