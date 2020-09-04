"""
Speaker db - Model
"""

from db.crud import CRUD


###########################################
##           Speakers CRUD ORM           ##
###########################################

COLLECTION_NAME = "speakers"
SpeakerModel = CRUD(COLLECTION_NAME)
