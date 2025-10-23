from pymongo import MongoClient
import gridfs
from backend.config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
fs = gridfs.GridFS(db)

parsed_collection = db["parsed_resumes"]