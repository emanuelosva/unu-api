"""
Db - Monglo Client instance and DB connection.
"""

# built-in imports
import json

# external imports
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
from bson import BSON

# module imports
from config import settings


###########################################
##             DB Connection             ##
###########################################

CLUSTER = settings.DB_CLUSTER
NAME = settings.DB_NAME
USER = settings.DB_USERNAME
PASSWORD = settings.DB_PASSWORD
CONFIG = "retryWrites=true&w=majority"
connection_str = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}/{NAME}?{CONFIG}"

# Get DB
client = AsyncIOMotorClient(connection_str)
db = client[settings.DB_NAME]


###########################################
##         Collection Instance           ##
###########################################


def get_collection(collection_name: str):
    """
    Return a mongo db collection instance.

    Params
    ------
    collection_name: str
        The mongo db collection name.

    Returns
    -------
    collection: Class
        The mongo db collection instance
    """

    collection = db[collection_name]
    return collection


###########################################
##             Parser Functions          ##
###########################################


def jsonify(data: BSON) -> dict:
    """
    Dumps a bson to json object.

    Params
    ------
    data: bson
        The mongo db bson data.

    Returns
    -------
    json_object: json
        The mongo data dumped to a json object
    """

    return json.loads(dumps(data))
