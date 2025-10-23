from fastapi import FastAPI
from backend.routes import upload, resumes
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Resume Backend")

# Register routes
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")