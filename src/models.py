from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, root_validator


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class City(BaseModel):
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

class UsersRequestByAge(BaseModel):
    min_age: Optional[int] = None
    max_age: Optional[int] = None

    @root_validator()
    def max_age_ge_min_age(cls, values):
        min_age =  values.get('min_age')
        max_age = values.get('min_age')
        if min_age is not None and max_age is not None:
            assert min_age <= max_age
        return values

    @root_validator()
    def age_ge_0(cls, values):
        min_age =  values.get('min_age')
        if min_age is not None:
            assert min_age >= 0

        max_age = values.get('min_age')
        if max_age is not None:
            assert max_age >= 0
        return values


class Picnic(BaseModel):
    id: int
    city_id: int
    time: datetime

    class Config:
        orm_mode = True