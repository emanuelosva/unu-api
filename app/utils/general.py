"""
General - Functionalities
"""

# module imports
from storage.service import upload_file


def store_file(file_b64: str = None, file: str = None) -> str:
    """
    Validate if is needed to generate a new upload.
    """
    if file:
        url = upload_file(file=file)
        return url

    url = file_b64
    if file_b64.startswith("data:"):
        url = upload_file(file_base64=file_b64)

    return url
