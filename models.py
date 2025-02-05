from uuid import UUID
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int
    graduated: bool

class UserRead(UserCreate):
    id: UUID

class UserUpdate(UserCreate):
    id: UUID
