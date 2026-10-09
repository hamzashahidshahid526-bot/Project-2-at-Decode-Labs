
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str = Field(..., description="Email must be unique")
    age: int = Field(..., ge=0, description="Age must be >= 0")

class UserResponse(BaseModel):
    id: int
    email: str
    age: int

    class Config:
        from_attributes = True
