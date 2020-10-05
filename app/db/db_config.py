"""
DB Config.
"""

from config import settings


TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": settings.DB_URL,
    },
    "apps": {
        "models": {
            "models": [
                "api.v1.users.models"
            ],
            "default_connection": "default",
        },
    },
}
