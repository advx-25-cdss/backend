from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import settings
import logging


class DataBase:
    client: AsyncIOMotorClient = None  # type: ignore
    cdss: AsyncIOMotorDatabase = None  # type: ignore


db = DataBase()


async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URI, maxPoolSize=10, minPoolSize=10)
    db.cdss = db.client.get_database("cdss")
    logging.info("connected to zvms...")


async def close_mongo_connection():
    logging.info("closing connection...")
    db.client.close()
    logging.info("closed connection")
