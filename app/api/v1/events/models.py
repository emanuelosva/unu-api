"""
Events db - Model
"""

from db.crud import CRUD


###########################################
##           Events CRUD ORM             ##
###########################################

COLLECTION_NAME = "events"
EventsModel = CRUD(COLLECTION_NAME)
