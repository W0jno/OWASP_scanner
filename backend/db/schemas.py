from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional

""" class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str # should be hashed in the database
    class Config:
        orm_mode = True """

class ScanCreate(BaseModel):
    #user_id: int
    url: str = Field(..., min_length=5, max_length=200)
    status: Optional[str] = Field(..., min_length=3, max_length=50)
    result: Optional[str] = Field(..., max_length=2000)

class ScanOut(BaseModel):
    id: int
    #user_id: int
    url: str
    status: Optional[str]
    result: Optional[str]
    class Config:
        orm_mode = True


class VulnerabilityCreate(BaseModel):
    scan_id: int
    vulnerability_type: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=2000)
    severity: str = Field(..., min_length=3, max_length=50)

class VulnerabilityOut(BaseModel):
    id: int
    scan_id: int
    vulnerability_type: str
    description: str
    severity: str
    class Config:
        orm_mode = True