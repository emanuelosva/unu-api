"""
DB Config.
"""

from config import settings

#####################################
# TORTOISE CONFIG FOR MANAGE MODELS #
#####################################

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": settings.DB_URL,
    },
    "apps": {
        "models": {
            "models": settings.DB_MODELS,
        },
    },
}
