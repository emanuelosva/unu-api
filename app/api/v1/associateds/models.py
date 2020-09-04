"""
Associateds db - Model
"""

from db.crud import CRUD


###########################################
##          Associateds CRUD ORM         ##
###########################################

COLLECTION_NAME = "associateds"
AssociatedModel = CRUD(COLLECTION_NAME)
