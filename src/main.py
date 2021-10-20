import datetime as dt
from typing import Optional
from fastapi import FastAPI, HTTPException, Query,  Depends
from database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from models import RegisterUserRequest, UserModel, CityRequest, \
    CityModel, UsersRequestByAge, UsersResponse,\
    RegisterCity, PicnicRequest, PicnicsResponse,\
    CitiesResponse, RegisterPicnic, PicnicModel, \
    RegisterRegisterPicnic, RegisterPicnicModel

app = FastAPI()



@app.post('/city/', summary='Create City', description='Создание города по его названию')
def create_city(city: RegisterCity):

    city_object = Session().query(City).filter(City.name == city.name).first()
    if city_object is None:
        city_object = City(name=city.name)
        s = Session()
        s.add(city_object)
        s.commit()

    return CityModel.from_orm(city_object)


@app.get('/cities/', summary='Get Cities')
def cities_list(q: CityRequest = Depends(CityRequest)):
    """
    Получение списка городов
    """
    cities = Session().query(City)
    
    if q.name is not None:
        cities = cities.filter(City.name == q.name)
    
    cities = cities.all()

    return CitiesResponse.from_orm(cities)


@app.get('/users/', summary='')
def users_list(age_range: UsersRequestByAge = Depends(UsersRequestByAge)):
    """
    Список пользователей
    """
    min_age, max_age = age_range.min_age, age_range.max_age 
       
    users = Session().query(User)

    if min_age is not None:
        users = users.filter(User.age >= min_age)
    
    if max_age is not None:
        users = users.filter(User.age <= max_age)

    users = users.all()

    return UsersResponse.from_orm(users)


@app.post('/user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(picnic: PicnicRequest = Depends(PicnicRequest)):
    """
    Список всех пикников
    """
    datetime, past = picnic.datetime, picnic.past
    
    picnics = Session().query(Picnic)
    
    if datetime is not None and past:
        picnics = picnics.filter(Picnic.time <= datetime)

    if datetime is not None and not past:
        picnics = picnics.filter(Picnic.time == datetime)

    picnics = picnics.all()

    return PicnicsResponse.from_orm(picnics)

@app.post('/picnic/', summary='Picnic Add', tags=['picnic'])
def picnic_add(param: RegisterPicnic = Depends(RegisterPicnic)):
    
    city_id, datetime = param.city_id, param.datetime

    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return PicnicModel.from_orm(p)


@app.post('/picnic_registration/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(param: RegisterRegisterPicnic = Depends(RegisterRegisterPicnic)):
    """
    Регистрация пользователя на пикник
    
    """
    user_id, picnic_id = param.user_id, param.picnic_id

    p_r = PicnicRegistration(user_id=user_id, 
                             picnic_id=picnic_id)

    s = Session()
    s.add(p_r)
    s.commit()

    return RegisterPicnicModel.from_orm(p_r)

