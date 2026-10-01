import os
import json
import logging
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger("db")

MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = "travel_planner"

class FileFallbackCollection:
    """Simulates a MongoDB async collection using a local JSON file."""
    def __init__(self, filename: str, collection_name: str):
        self.filepath = filename
        self.collection_name = collection_name
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump({}, f)
        
        # Ensure collection exists in file
        with open(self.filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        
        if self.collection_name not in data:
            data[self.collection_name] = []
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)

    def _read_data(self) -> list:
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return data.get(self.collection_name, [])

    def _write_data(self, collection_data: list):
        with open(self.filepath, "r") as f:
            data = json.load(f)
        data[self.collection_name] = collection_data
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    async def find_one(self, query: dict) -> dict:
        collection_data = self._read_data()
        for doc in collection_data:
            match = True
            for k, v in query.items():
                if k in ("_id", "id"):
                    doc_id = str(doc.get("_id") or doc.get("id") or "")
                    if doc_id != str(v):
                        match = False
                elif k == "user_id":
                    doc_user = str(doc.get("user_id") or "")
                    if doc_user != str(v):
                        match = False
                elif doc.get(k) != v:
                    match = False
            if match:
                doc_id = str(doc.get("_id") or doc.get("id") or "")
                if doc_id:
                    doc["_id"] = doc_id
                    doc["id"] = doc_id
                return doc
        return None

    async def find(self, query: dict = None) -> list:
        collection_data = self._read_data()
        if not query:
            for doc in collection_data:
                doc_id = str(doc.get("_id") or doc.get("id") or "")
                if doc_id:
                    doc["_id"] = doc_id
                    doc["id"] = doc_id
            return collection_data
        
        results = []
        for doc in collection_data:
            match = True
            for k, v in query.items():
                if k in ("_id", "id"):
                    doc_id = str(doc.get("_id") or doc.get("id") or "")
                    if doc_id != str(v):
                        match = False
                elif k == "user_id":
                    doc_user = str(doc.get("user_id") or "")
                    if doc_user != str(v):
                        match = False
                elif doc.get(k) != v:
                    match = False
            if match:
                doc_id = str(doc.get("_id") or doc.get("id") or "")
                if doc_id:
                    doc["_id"] = doc_id
                    doc["id"] = doc_id
                results.append(doc)
        return results

    async def insert_one(self, document: dict):
        collection_data = self._read_data()
        doc_id = str(document.get("_id") or document.get("id") or ObjectId())
        document["_id"] = doc_id
        document["id"] = doc_id
            
        collection_data.append(document)
        self._write_data(collection_data)
        
        class InsertResult:
            inserted_id = doc_id
        return InsertResult()

    async def update_one(self, query: dict, update: dict, upsert: bool = False):
        collection_data = self._read_data()
        update_fields = update.get("$set", {})
        
        updated = False
        for doc in collection_data:
            match = True
            for k, v in query.items():
                if k in ("_id", "id"):
                    doc_id = str(doc.get("_id") or doc.get("id") or "")
                    if doc_id != str(v):
                        match = False
                elif k == "user_id":
                    doc_user = str(doc.get("user_id") or "")
                    if doc_user != str(v):
                        match = False
                elif doc.get(k) != v:
                    match = False
            if match:
                doc.update(update_fields)
                doc_id = str(doc.get("_id") or doc.get("id") or "")
                if doc_id:
                    doc["_id"] = doc_id
                    doc["id"] = doc_id
                updated = True
                break
                
        if not updated and upsert:
            new_doc = {**query, **update_fields}
            doc_id = str(new_doc.get("_id") or new_doc.get("id") or ObjectId())
            new_doc["_id"] = doc_id
            new_doc["id"] = doc_id
            collection_data.append(new_doc)
            
        self._write_data(collection_data)
        
        class UpdateResult:
            matched_count = 1 if updated else 0
            modified_count = 1 if updated else 0
        return UpdateResult()

    async def delete_one(self, query: dict):
        collection_data = self._read_data()
        
        new_data = []
        deleted = False
        for doc in collection_data:
            match = True
            for k, v in query.items():
                if k in ("_id", "id"):
                    doc_id = str(doc.get("_id") or doc.get("id") or "")
                    if doc_id != str(v):
                        match = False
                elif k == "user_id":
                    doc_user = str(doc.get("user_id") or "")
                    if doc_user != str(v):
                        match = False
                elif doc.get(k) != v:
                    match = False
            if match and not deleted:
                deleted = True
                continue
            new_data.append(doc)
            
        self._write_data(new_data)
        
        class DeleteResult:
            deleted_count = 1 if deleted else 0
        return DeleteResult()


class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.use_fallback = True
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.fallback_file = os.path.join(base_dir, "local_db.json")

    def connect(self):
        if MONGODB_URI:
            try:
                # Set a short timeout for quick fallback check
                self.client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
                # Force connection check
                self.db = self.client[DB_NAME]
                self.use_fallback = False
                print("MongoDB Atlas Connected Successfully.")
            except (ConnectionFailure, Exception) as e:
                print(f"MongoDB connection failed: {e}. Falling back to Local JSON Database.")
                self.use_fallback = True
        else:
            print("No MONGODB_URI provided. Falling back to Local JSON Database (local_db.json).")
            self.use_fallback = True

    def get_collection(self, name: str):
        if self.use_fallback:
            return FileFallbackCollection(self.fallback_file, name)
        return self.db[name]

db_connection = DatabaseConnection()
db_connection.connect()

# Collection helpers
def get_users_collection():
    return db_connection.get_collection("users")

def get_trips_collection():
    return db_connection.get_collection("trips")
