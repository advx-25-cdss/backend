from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from models.ehr_models import *
from database import db
from datetime import datetime, timezone

class EHRService:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return db.cdss.get_collection(self.collection_name)

    async def create(self, data: dict) -> dict:
        """Create a new record"""
        if "_id" in data and data["_id"] is None:
            del data["_id"]

        # Generate a UUID string for _id if not provided
        if "_id" not in data:
            data["_id"] = ObjectId()

        data["created_at"] = datetime.now(timezone.utc)
        data["updated_at"] = datetime.now(timezone.utc)

        await self.collection.insert_one(data)
        created_record = await self.collection.find_one({"_id": data["_id"]})
        return created_record

    async def get_by_id(self, record_id: str) -> Optional[dict]:
        """Get a record by ID"""
        return await self.collection.find_one({"_id": record_id})

    async def get_by_patient_id(self, patient_id: str) -> List[dict]:
        """Get all records for a specific patient"""
        cursor = self.collection.find({"patient_id": patient_id})
        return await cursor.to_list(length=None)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all records with pagination"""
        cursor = self.collection.find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(self, record_id: str, data: dict) -> Optional[dict]:
        """Update a record"""
        data["updated_at"] = datetime.now(timezone.utc)

        # Remove None values and _id from update data
        update_data = {k: v for k, v in data.items() if v is not None and k != "_id"}

        await self.collection.update_one(
            {"_id": record_id},
            {"$set": update_data}
        )

        return await self.collection.find_one({"_id": record_id})

    async def delete(self, record_id: str) -> bool:
        """Delete a record"""
        result = await self.collection.delete_one({"_id": record_id})
        return result.deleted_count > 0

    async def search(self, query: dict, skip: int = 0, limit: int = 100) -> List[dict]:
        """Search records based on query"""
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def count(self, query: dict = None) -> int:
        """Count records matching query"""
        if query is None:
            query = {}
        return await self.collection.count_documents(query)

# Service instances for each collection
demographics_service = EHRService("demographics")
menstrual_service = EHRService("menstrual")
obstetric_service = EHRService("obstetric")
marital_service = EHRService("marital")
history_present_illness_service = EHRService("history_present_illness")
past_medical_history_service = EHRService("past_medical_history")
family_history_service = EHRService("family_history")
medication_history_service = EHRService("medication_history")
allergy_history_service = EHRService("allergy_history")
social_history_service = EHRService("social_history")
vital_signs_service = EHRService("vital_signs")
