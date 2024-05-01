# app/auth/get_users.py

from fastapi import APIRouter, HTTPException

from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

from bson import ObjectId


async def find_user_by_username(username):
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]

    users_collection = db["users"]

    user = await users_collection.find_one({"username": username})

    return {
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    }


@router.get("/get-users")
async def get_users():
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]

    users_collection = db["users"]

    # Get all users
    users = []
    async for user in users_collection.find():
        users.append({
            "username": user["username"],
            "email": user["email"]
        })

    return {"users": users}

