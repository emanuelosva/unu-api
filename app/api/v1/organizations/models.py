"""
Organization db - Model
"""

from db.crud import CRUD


###########################################
##        Organizations CRUD ORM         ##
###########################################

COLLECTION_NAME = "organizations"
OrganizationModel = CRUD(COLLECTION_NAME)
