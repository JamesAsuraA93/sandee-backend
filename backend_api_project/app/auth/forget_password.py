# # app/auth/forget_password.py
# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/forget-password")
# async def forget_password(email: str):
#     # Generate reset password token and send it to user's email
#     # Update user document in MongoDB with reset password token and expiration time
#     pass


# app/auth/forget_password.py
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

@router.post("/forget-password")
async def forget_password(email: str):
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]
    users_collection = db["users"]
    
    # Find user by email in MongoDB
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate reset password token and send it to user's email (not implemented here)
    # Update user document in MongoDB with reset password token and expiration time (not implemented here)
    
    # Return success message
    return {"message": "Reset password token sent to email"}
