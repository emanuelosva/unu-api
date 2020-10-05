"""
Main app entry point.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from db.db_config import TORTOISE_ORM_CONFIG

from api import api_router
from config import settings

################
# App Settings #
################

app = FastAPI(
    title=settings.APP_NAME,
    description="An awesome app to create and manage your events.",
    version="1.0",
)


###############
# DB Settings #
###############

register_tortoise(app, config=TORTOISE_ORM_CONFIG, generate_schemas=True)

###############
# Middlewares #
###############

if len(settings.CORS_ORIGIN) != 0:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


##########
# Router #
##########

app.include_router(api_router, prefix="/api")
