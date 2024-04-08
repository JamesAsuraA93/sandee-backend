# # app/files/upload.py
# from fastapi import APIRouter, UploadFile, File
# import os

# router = APIRouter()

# UPLOAD_DIRECTORY = "../backend_api_project/data/uploads"  # Adjust path as needed

# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())
#     # Save file metadata or perform additional operations as needed
#     return {"filename": file.filename}


# app/files/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

UPLOAD_DIRECTORY = "../app/data/uploads"  # Adjust path as needed

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["file_db"]
    files_collection = db["files"]

    try:
        # print current working directory
        # print(os.getcwd())
        # Save file to disk
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Save file metadata to MongoDB
        file_metadata = {"filename": file.filename, "path": file_path}
        result = await files_collection.insert_one(file_metadata)

        # Return success message
        return {"message": "File uploaded successfully"}
    except Exception as e:
        # If an error occurs during file upload, raise HTTPException
        raise HTTPException(status_code=500, detail=str(e))
