"""
Main app entry point.
"""

# external imports
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# module imports
from api import api_router
from config import settings  # pylint: disable-msg=E0611

###########################################
##              App Settings             ##
###########################################

app = FastAPI(
    title=settings.APP_NAME,
    description="An awesome app to create and manage your events.",
    version="1.0",
)

###########################################
##               Middlewares             ##
###########################################

if len(settings.CORS_ORIGIN) != 0:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

###########################################
##                 Router                ##
###########################################

app.include_router(api_router, prefix="/api")
