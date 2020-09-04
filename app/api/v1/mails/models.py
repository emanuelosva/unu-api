"""
Mails db - Model
"""

from db.crud import CRUD

COLLECTION_NAME = "participants"
MailsModel = CRUD(COLLECTION_NAME)
