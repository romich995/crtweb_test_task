import datetime as dt
from fastapi import FastAPI, HTTPException, Query
from database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from external_requests import OpenWeatherMapAPI
from models import RegisterUserRequest, UserModel

app = FastAPI()


@app.get('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = OpenWeatherMapAPI()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.post('/get-cities/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    cities = Session().query(City)
    
    if q is not None:
        cities = cities.filter(City.name == q.capitalize())
    
    cities = cities.all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]


@app.post('/users-list/', summary='')
def users_list(min_age: int = Query(description="Минималььный возвраст", \
                                    default=None),\
               max_age: int = Query(description="Максимальный возраст",\
                                    default=None)):
    """
    Список пользователей
    """
    if max_age is not None and min_age is not None and max_age < min_age:
        return []
       
    users = Session().query(User)

    if min_age is not None:
        users = users.filter(User.age >= min_age)
    
    if max_age is not None:
        users = users.filter(User.age <= max_age)

    users = users.all()      
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.get('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    
    if city_id is None or datetime is None:
        raise HTTPException(status_code=400, 
            detail='Необходимы оба параметра city_id и datetime')

    city = Session().query(City).filter(City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=400,
                detail='Невалидный город')

    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': city.name,
        'time': p.time,
    }


@app.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(user_id: int = None, picnic_id: int = None):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    # TODO: Сделать логику

    if user_id is None or picnic_id is None:
        raise HTTPException(status_code=400, 
            detail='Необходимы оба параметра user_id и picnic_id')

    user = Session().query(User).filter(User.id == city_id).first()

    if user is None:
        raise HTTPException(status_code=400,
                detail='Невалидный пользователь')

    picnic = Session().query(Picnic).filter(Picnic.id == picnic_id).first()

    if picnic is None:
        raise HTTPException(status_code=400,
                detail='Невалидный пикник')


    p_r = PicnicRegistration(user_id=user_id, 
                             picnic_id=picnic_id)

    s = Session()
    s.add(p)
    s.commit()

    return dict(id=p_r.id,
                user_id=p_r.user_id,
                picnic_id=p_r.picnic_id)

