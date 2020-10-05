"""
Main API - Router
"""

from fastapi import APIRouter

from api.v1 import v1_router


################
# API - ROUTER #
################

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")
