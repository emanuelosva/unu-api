"""
Google Cloud Storage - Connection.
"""

from google.cloud import storage

from config import settings


#####################
# Bucket Connection #
#####################


def get_storage_bucket():
    """
    Return a GCP bucket-storage client.
    """
    buckent_name = settings.GOOGLE_STORAGE_BUCKET

    client = storage.Client()
    bucket = client.bucket(buckent_name)
    return bucket
