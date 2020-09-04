"""
Participants db - Model
"""

from db.crud import CRUD


###########################################
##           Events CRUD ORM             ##
###########################################

COLLECTION_NAME = "participants"
ParticipantsModel = CRUD(COLLECTION_NAME)
