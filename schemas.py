from typing import List, Optional
import strawberry

from models import WeatherData as WeatherDataModel
from models import CityData as CityModel
from models import User as UserModel

@strawberry.experimental.pydantic.type(model=WeatherDataModel, 
                                       fields=["date_time", "temperature", "humidity"])
class WeatherData:
    date_time = str
    temperature = float
    humidity = float

@strawberry.experimental.pydantic.type(model=CityModel, fields=["name", "weather_data"])
class CityDataType:
    name = str
    weather_data = List[WeatherData]

@strawberry.experimental.pydantic.type(model=UserModel, fields=["first_name", "last_name"])
class User:
   first_name = str
   last_name = str

   favorites = Optional[List[CityDataType]]

   @strawberry.field
   async def favorites(self, info) -> List[CityDataType]:
       return [CityDataType(name=city.name) for city in self.favorites]

@strawberry.input
class WeatherDataInput:
    date_time: str
    temperature: Optional[float] = strawberry.UNSET
    humidity: Optional[float] = strawberry.UNSET

@strawberry.type
class UserNotFound:
    message: str = "Couldn't find an user with the given name"

@strawberry.type
class UserAlreadyExists:
    message: str = "This user already exists"

@strawberry.type
class UserHasNoFavorites:
    message: str = "This user has no favorites"

@strawberry.type
class IDType:
    id: strawberry.ID


@strawberry.type
class UserResponse:
    id: strawberry.ID
    first_name: str
    last_name: str

