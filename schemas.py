from typing import List, Optional
import strawberry

from models import WeatherData as WeatherDataModel
from models import CityData as CityModel
from models import User as UserModel

@strawberry.experimental.pydantic.type(model=WeatherDataModel, 
                                       fields=["date_time", "temperature", "humidity"])
class WeatherData:
    date_time = int
    temperature = float
    humidity = float

@strawberry.experimental.pydantic.type(model=CityModel, fields=["name", "weather_data"])
class CityDataType:
    name = str
    weather_data = List[WeatherData]

@strawberry.experimental.pydantic.type(model=UserModel, fields=["first_name", "last_name"])
class User:
   id = strawberry.ID
   first_name = str
   last_name = str
   favorite = Optional [List[CityDataType]]

@strawberry.input
class WeatherDataInput:
    date_time: int
    temperature: Optional[float] = strawberry.UNSET
    humidity: Optional[float] = strawberry.UNSET

@strawberry.type
class UserNotFound:
    message: str = "Couldn't find an user with the given name"

@strawberry.type
class UserHasNoFavorites:
    message: str = "This user has no favorites"



