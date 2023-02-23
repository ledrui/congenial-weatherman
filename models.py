import os
from os import getenv

from typing import List
from typing import Optional
import uuid

from odmantic import Field, Model


class WeatherData(Model):
    date_time: int = Field(required=True)
    temperature: float = Field(required=True)
    humidity: float = Field(required=True)

class CityData(Model):
    name: str = Field(required=True)
    weather_data : List[WeatherData] = Field(default_factory=list)

class User(Model):
    first_name: str 
    last_name: str
    favorite: Optional[List[CityData]] = Field(default_factory=list)

