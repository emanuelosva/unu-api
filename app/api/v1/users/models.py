"""
User db - Model
"""

from db.crud import CRUD


###########################################
##             Users CRUD ORM            ##
###########################################

COLLECTION_NAME = "users"
UserModel = CRUD(COLLECTION_NAME)
