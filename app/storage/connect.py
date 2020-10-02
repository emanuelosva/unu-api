"""
Google Cloud Storage - Connection.
"""

# external imports
from google.cloud import storage

# module imports
from config import settings


###########################################
##           Bucket Connection           ##
###########################################


def get_storage_bucket():
    """
    Return a GCP bucket-storage client.
    """
    buckent_name = settings.GOOGLE_STORAGE_BUCKET

    client = storage.Client()
    bucket = client.bucket(buckent_name)
    return bucket
