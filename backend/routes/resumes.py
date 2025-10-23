from fastapi import APIRouter
from backend.database import db

router = APIRouter()

@router.get("/")
def list_resumes():
    resumes = list(db.resumes.find({}, {"filename": 1, "content": 1}))
    for r in resumes:
        r["_id"] = str(r["_id"])
    return resumes
