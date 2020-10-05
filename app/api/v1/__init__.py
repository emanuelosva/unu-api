"""
API V1 - Router
"""

# external imports
from fastapi import APIRouter

# module imports
from api.v1.users.routes import router as users_router

# from api.v1.organizations.routes import router as organization_router
# from api.v1.events.routes import router as events_router
# from api.v1.associateds.routes import router as associateds_router
# from api.v1.speakers.routes import router as speakers_router
# from api.v1.agenda.routes import router as agenda_router
# from api.v1.participants.routes import router as participants_router
# from api.v1.mails.routes import router as mails_router


###########################################
##             Version 1 Router          ##
###########################################

v1_router = APIRouter()

# --- User router --- #
v1_router.include_router(users_router, prefix="/users", tags=["Users"])

# --- Organizations router --- #
# v1_router.include_router(
#     organization_router, prefix="/organizations", tags=["Organizations"]
# )

# # --- Events router --- #
# v1_router.include_router(events_router, prefix="/events", tags=["Events"])

# # --- Associateds router --- #
# v1_router.include_router(
#     associateds_router, prefix="/associateds", tags=["Associateds"]
# )

# # --- Speakers router --- #
# v1_router.include_router(speakers_router, prefix="/speakers", tags=["Speakers"])

# # --- Agenda router --- #
# v1_router.include_router(agenda_router, prefix="/agenda", tags=["Agenda"])

# # --- Mails router --- #
# v1_router.include_router(mails_router, prefix="/mails", tags=["Mails"])

# # --- Participants router --- #
# v1_router.include_router(
#     participants_router, prefix="/participants", tags=["Participants"]
# )
