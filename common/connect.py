from pymongo import MongoClient

from django.conf import settings

client = MongoClient(settings.MONGO_URI)

def get_db():
    """
    Get database from MongoDB.

        Args:
             db_name (str): Database name.

        Returns:
            Mongo Database.
    """
    db = client[settings.MONGO_DATABASE]
    return db

