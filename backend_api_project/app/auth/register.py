# # app/auth/register.py
# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/register")
# async def register(username: str, password: str, email: str):
#     # Register user here (create a new user document in MongoDB)
#     pass


# app/auth/register.py
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()


from bson import ObjectId

@router.post("/register")
async def register(username: str, password: str, email: str):
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]
    users_collection = db["users"]
    
    # Check if username or email already exists
    existing_user = await users_collection.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user document
    try:
        user_data = {
            # gen new id by group all with username and eamil and plus the count of the users
            # "_id": ObjectId(
            #     str(hash(username + email + str(await users_collection.count_documents({}))))
            # ),
            "username": username, 
            "password": password, 
            "email": email}
        result = await users_collection.insert_one(user_data)
        inserted_id = result.inserted_id
        # Return the inserted_id if needed

        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="User registration failed")
        else:
            print("User registration success")
            return str(inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User registration failed: {str(e)}")
    # result = await users_collection.insert_one(user_data)
    # if not result.acknowledged:
    #     raise HTTPException(status_code=500, detail="User registration failed")
    
    
    # Return newly registered user data
    return user_data
