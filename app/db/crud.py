"""
Db - CRUD class.
"""

# build-in imports
from typing import List

# module imports
from logger.main import ErrorLogger
from .db import get_collection, jsonify


###########################################
##             Error Logger              ##
###########################################
error_logger = ErrorLogger(get_collection=get_collection)


###########################################
##           CRUD Operations             ##
###########################################


class CRUD:
    """
    Crud operations.

    Params:
    ------
    collection: mongo_collection
        The mongo collection for CRUD
    """

    def __init__(self, collection):
        """
        Collection injection on initialzation.
        """
        self._db = get_collection(collection)

    async def create(self, document_data: dict) -> str:
        """
        Create a new document in collection.
        """
        try:
            created = await self._db.insert_one(document_data)
        except Exception as ex:
            await error_logger.register(ex)
        return str(created.inserted_id)

    async def update(self, query: dict, document_data: dict, many: bool = False) -> int:
        """
        Update an existing document.
        """
        try:
            if many:
                updated = await self._db.update_many(query, {"$set": document_data})
            else:
                updated = await self._db.update_one(query, {"$set": document_data})
        except Exception as ex:
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def add_to_set(self, query: dict, array_name: str, data: any) -> int:
        """
        Add a new item to a list within a document.
        """
        operation = {"$addToSet": {f"{array_name}": data}}
        try:
            updated = await self._db.update_one(query, operation)
        except Exception as ex:
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def push_nested(self, query: dict, path: str, data: any) -> int:
        """
        Insert a new document in nested element.
        """
        operation = {"$push": {f"{path}": data}}
        try:
            updated = await self._db.update_one(query, operation)
        except Exception as ex:
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def pull_array(
        self, query: dict, array_name: str, condition: dict, many: bool = False
    ) -> int:
        """
        Remove a item from a list that matches the condition.
        """
        operation = {"$pull": {f"{array_name}": condition}}
        try:
            if many:
                updated = await self._db.update_many(query, operation)
            else:
                updated = await self._db.update_one(query, operation)
        except Exception as ex:
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def delete(self, query: dict, many: bool = False) -> int:
        """
        Delete a existing document.
        """
        try:
            if many:
                deleted = await self._db.delete_many(query)
            else:
                deleted = await self._db.delete_one(query)
        except Exception as ex:
            await error_logger.register(ex)
        return int(deleted.deleted_count)

    async def find(
        self,
        query: dict,
        only_one: bool = True,
        filters: List[str] = None,
        excludes: List[str] = None,
    ) -> dict:
        """
        Retrieve the data that matches with the query and the filters.
        """
        # Create the query filter
        query_filter = None
        if filters is not None:
            query_filter = self._generate_query_filter(filters)
        if excludes is not None:
            query_filter = self._generate_query_filter(excludes, excludes=True)

        try:
            # For find a single document
            if only_one:
                document = await self._db.find_one(query, query_filter)
                return jsonify(document)

            # For find multiple documents
            cursor = self._db.find(query, query_filter)
            items = []
            for document in await cursor.to_list(length=100):
                items.append(document)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)
        return items

    async def find_from_foregyn_key(
        self, collection: str, foregyn_keys: List[str]
    ) -> List[dict]:
        """
        Find a documents associates with the passed foregyn key.
        """
        collection = get_collection(collection)
        query = {"uuid": {"$in": foregyn_keys}}
        cursor = collection.find(query, {"_id": 0})
        associated_docs = []
        for document in await cursor.to_list(length=100):
            associated_docs.append(document)
        return associated_docs

    def _generate_query_filter(
        self, filter_list: list = None, excludes: bool = False
    ) -> dict:
        """
        Generate a dict with the correct mongo query filter
        """

        objet_filter = {}
        if filter_list is not None:
            for key in filter_list:
                if excludes:
                    objet_filter[key] = 0
                else:
                    objet_filter[key] = 1

        return objet_filter
