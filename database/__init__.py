import logging
from config import MONGODB_URI, MONGODB_DB_NAME

logger = logging.getLogger("facultyflow.db")

_store_instance = None

def get_store():
    global _store_instance
    if _store_instance is not None:
        return _store_instance

    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI is not configured in .env. MongoDB is required for all data storage.")

    try:
        from database.mongo_store import MongoDataStore
        logger.info("Connecting strictly to MongoDB Atlas...")
        _store_instance = MongoDataStore(MONGODB_URI, MONGODB_DB_NAME)
        logger.info("Successfully connected to MongoDB Atlas.")
        return _store_instance
    except Exception as e:
        logger.error(f"Fatal: Could not connect to MongoDB Atlas ({e}).")
        raise RuntimeError(f"MongoDB connection failed: {e}. Local fallback is disabled.")

