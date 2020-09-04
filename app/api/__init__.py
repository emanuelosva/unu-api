"""
Main API - Router
"""

# external imports
from fastapi import APIRouter

# module imports
from api.v1 import v1_router


###########################################
##               API - ROUTER            ##
###########################################

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")
