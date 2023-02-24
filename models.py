from os import getenv

from typing import List
from typing import Optional

from odmantic import Field, Model, EmbeddedModel


class WeatherData(EmbeddedModel):
    date_time: str
    temperature: float 
    humidity: float

class CityData(EmbeddedModel):
    name: str = Field(required=True)
    weather_data : List[WeatherData] = Field(default_factory=list)

class User(Model):
    first_name: str
    last_name: Optional[str]
    favorites: Optional[List[CityData]] = []

