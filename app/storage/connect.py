"""
Google Cloud Storage - Connection.
"""
# external imports
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

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
    try:
        client = storage.Client()
        bucket = client.bucket(buckent_name)
    except DefaultCredentialsError:
        client = storage.Client(settings.GOOGLE_APPLICATION_CREDENTIALS)
    except Exception:  # pylint: disable-msg=W0703
        return False
    bucket = client.bucket(buckent_name)
    return bucket
