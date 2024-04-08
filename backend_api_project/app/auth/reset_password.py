# # app/auth/reset_password.py
# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/reset-password")
# async def reset_password(token: str, new_password: str):
#     # Check if reset password token is valid and not expired
#     # If valid, update user's password in MongoDB
#     pass


# app/auth/reset_password.py
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]
    users_collection = db["users"]
    
    # Verify token and update user's password in MongoDB (not implemented here)
    
    # Return success message
    return {"message": "Password reset successful"}
