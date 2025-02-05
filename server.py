import base64
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID, uuid4
import shelve as Shelf
from fastapi.responses import RedirectResponse

from db import session_factory

from models import *

class UserCreate(BaseModel):
    name: str
    age: int
    graduated: bool


class UserRead(UserCreate):
    id: UUID
    profile_picture: bytes = None

    def set_profile_picture(self, image_bytes: bytes):
        """Encode bytes as Base64 string"""
        self.profile_picture = base64.b64encode(image_bytes).decode("utf-8")


class UserUpdate(UserCreate):
    profile_picture: bytes = None

    def set_profile_picture(self, image_bytes: bytes):
        """Encode bytes as Base64 string"""
        self.profile_picture = base64.b64encode(image_bytes).decode("utf-8")


# TODO: paste your routers from previous lab in here

# TODO: make the routers async 


app = FastAPI(
    title="Lab3 - User Management API",
    description="User CRUD operations using FastAPI and shelve",
    docs_url="/docs",  # Swagger UI URL
)

@app.get("/", include_in_schema=False)
async def root():
    """Redirects to the Swagger UI"""
    return RedirectResponse(url="/docs")

@app.get("/users/")
async def get_all_users(db: Shelf = Depends(session_factory)):
    return list(db.values())

@app.get("/users/{user_id}")
async def get_user(user_id: UUID, db: Shelf = Depends(session_factory)):
    try:
        return db[str(user_id)]
    except KeyError:
        raise HTTPException(status_code=409, detail=f"User not found under id {user_id}!")

@app.post("/users/")
async def create_user(user: UserCreate, db: Shelf = Depends(session_factory)):
    new_user = UserRead(id=uuid4(), **user.model_dump())
    db[str(new_user.id)] = new_user
    return new_user

@app.put("/users/{user_id}")
async def update_user(user_id: UUID, user: UserUpdate, db: Shelf = Depends(session_factory)):
    try:
        db[str(user_id)] = user
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User not found under id <{user_id}>!")
    return user

@app.patch("/users/{user_id}")
async def update_user_graduated(user_id: UUID, graduated: bool, db: Shelf = Depends(session_factory)):
    try:
        user: UserUpdate = db[str(user_id)]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User not found under id <{user_id}>!")
    user.graduated = ~graduated
    db[str(user_id)] = user
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: Shelf = Depends(session_factory)):
    try:
        del db[str(user_id)]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User not found under id <{user_id}>!")


# @app.post("/user/{user_id}/profile_picture/")
# async def set_profile_picture(user_id: UUID, file: UploadFile = File(...)):
#     with Shelf.open("users") as users:
#         user = users.get(str(user_id))
#         if user is None:
#             return {"error": "User not found"}

#         image_bytes = await file.read()
#         user.set_profile_picture(image_bytes)  # Convert to Base64
#         users[str(user_id)] = user  # Store back in shelve

#     return {"message": "Profile picture updated successfully"}

@app.post("/user/{user_id}/profile_picture/")
async def set_profile_picture(user_id: UUID, file: UploadFile = File(...), db: Shelf = Depends(session_factory)):
    if str(user_id) not in db:
        raise HTTPException(status_code=404, detail=f"User not found under id {user_id}!")
    
    image_bytes = await file.read()

    user = db[str(user_id)]
    user.set_profile_picture(image_bytes)  # Convert image to Base64
    db[str(user_id)] = user  # Store back in shelve


    return {"message": "Profile picture updated dwcqfghhkpyfrdsghukt;oaejtjawegoergsuccessfully"}

