from pydantic import BaseModel
from datetime import datetime

class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class RegisterCity(BaseModel):
    name: str

class CityModel(BaseModel):
    id: int
    name: str
    weather: float

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True

class Picnic(BaseModel):
    id: int
    city_id: int
    time: datetime

    class Config:
        orm_mode = True