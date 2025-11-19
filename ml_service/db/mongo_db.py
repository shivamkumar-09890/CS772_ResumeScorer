from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from pymongo import MongoClient
import gridfs

class MongoConfig:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="resume_db"):
        self.uri = uri
        self.db_name = db_name
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

        self.fs = gridfs.GridFS(self.db)

        self.parsed_resume_collection = self.db["parsed_resume"]

class MongoClientWrapper:
    def __init__(self, config):
        self.config = config

    def get_all_resume_files(self):
        """Fetch all files stored in GridFS."""
        return list(self.config.db["fs.files"].find({}))

    def get_file_by_id(self, file_id: str):
        return self.config.fs.get(ObjectId(file_id))

    def store_parsed_resume(self, resume_id: str, parsed_text: str):
        """Insert parsed resume into parsed_resume collection."""
        doc = {
            "resume_id": resume_id,
            "parsed_text": parsed_text
        }

        # If resume already parsed → update instead of duplicate insertion
        return self.config.parsed_resume_collection.update_one(
            {"resume_id": resume_id},
            {"$set": doc},
            upsert=True
        )
