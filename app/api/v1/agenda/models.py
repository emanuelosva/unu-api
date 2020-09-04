"""
Agenda db - Model
"""

from db.crud import CRUD


###########################################
##           Events CRUD ORM             ##
###########################################

COLLECTION_NAME = "agenda"
AgendaModel = CRUD(COLLECTION_NAME)
