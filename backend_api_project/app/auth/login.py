# # app/auth/login.py
# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/login")
# async def login(username: str, password: str):
#     # Authenticate user here (check credentials against MongoDB)
#     # If authentication is successful, return user data with a token
#     # If authentication fails, return appropriate error message
#     pass


# app/auth/login.py
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

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

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str):
    
    print("username: ", username)
    print("password: ", password)
    
    try:


        user = await find_user_by_username(username)
        if user is not None:
            print("User found:", user)
        else:
            print("User not found")

        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        # Verify password
        print("user['password']: ", user["password"])
        if user["password"] != password:
            raise HTTPException(status_code=401, detail="Incorrect password")
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    
    # Find user by username in MongoDB
    # user = await users_collection.find_one({"username": username})
    # print("user: ", user['username'])
    
    
    # Return user data
    return {
        "username": user["username"],
        "email": user["email"]

    }
