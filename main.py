import datetime
import os
import time
from dotenv import load_dotenv
import json
import httplib2
from requests import HTTPError
import logging

import strawberry
from odmantic import ObjectId
import redis

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from models import WeatherData as WeatherDataModel
from models import CityData as CityModel
from models import User as UserModel

from db import engine
from schemas import User, CityDataType, UserResponse, WeatherData, WeatherDataInput
from utils.utils import *

cache = redis.Redis(host='redis', port=6379)

load_dotenv(".env")

WEATHER_API_ENDPOINT = os.environ["WEATHER_API_ENDPOINT"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info, first_name: Optional[str] = None, user_id: Optional[str] = None) -> UserResponse:
        
        if user_id:
            user = await engine.find_one(UserModel, UserModel.id == ObjectId(user_id))
        elif first_name:
            user = await engine.find(UserModel, UserModel.first_name == first_name)
        
        if not user:
            raise Exception(f"Couldn't find an user with the given name: {first_name}, or user_id: {user_id}")
        
        return UserResponse(id=strawberry.ID(user.id), first_name=user.first_name, last_name=user.last_name)
    
    @strawberry.field
    async def get_weather_by_city(self, info, city_name:str, date:Optional[str]) -> CityDataType:
        # Convert UTC time string to datetime object "YYYY-MM-DD HH:MM:SS" format

        # check if city data is in cache
        city_data = cache.get(city_name)
        if city_data and len(city_data):            
            city_data = json.loads(city_data)
            weather_data = [WeatherDataModel(date_time=data["date_time"], 
                                         temperature=data["temperature"], 
                                         humidity=data["humidity"]) for data in city_data]
            return CityDataType(name=city_name, weather_data=weather_data) 
                
        url = WEATHER_API_ENDPOINT + "/forecast?q=" + city_name + "&appid=" + WEATHER_API_KEY
        http_initializer = httplib2.Http()
        try:
            response, content = http_initializer.request(url,'GET')
        except Exception as e:
            raise HTTPError(f"Error while fetching data from OpenWeather API: {e}")
        
        utf_decoded_content = content.decode('utf-8')
        json_object = json.loads(utf_decoded_content)
        if json_object["cod"] != "200":
            raise Exception("City not found")
        
        city_data = []

        for data in json_object["list"]:
            thisdate = str(convert_unix_date_time_to_utc_date_time(data["dt"]))

            # check if date is in the same day ingnoring time
            if date and date.split(" ")[0] == thisdate.split(" ")[0]:
                city_data.append({
                        "date_time": thisdate,
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"]
                    })
            else:
                city_data.append({
                        "date_time": thisdate,
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"]
                    })
        
        weather_data = [WeatherDataModel(date_time=data["date_time"], 
                                         temperature=data["temperature"], 
                                         humidity=data["humidity"]) for data in city_data]
        
        city = CityModel(name=city_name, weather_data=weather_data)

        # set city data in cache
        json_city_data =json.dumps(city_data)
        cache.set(city_name, json_city_data)
     
        return CityDataType(name=city.name, weather_data=city.weather_data)
    
    @strawberry.field
    async def get_favorites(self, info, user_id: str, first_name: Optional[str] = None) -> List[CityDataType]:
        user = await engine.find_one(UserModel, UserModel.id == ObjectId(user_id))
        if not user:
            raise Exception("User not found")
        if not user.favorites:
            raise Exception("User has no favorites yet")
        
        response = [CityDataType(name=city.name, weather_data=city.weather_data) for city in user.favorites]
        return response
    
    @strawberry.field
    async def get_city_data(self, info, city_name: str) -> CityDataType:
        city_data = cache.get(city_name)
        if not city_data:
            raise Exception("City not found")
        city_data = json.loads(city_data)
        weather_data = [WeatherDataModel(date_time=data["date_time"], 
                                         temperature=data["temperature"], 
                                         humidity=data["humidity"]) for data in city_data]
        
        return CityDataType(name=city_name, weather_data=weather_data)
        
        
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_favorites(self, info, city:str, user_id:str, 
                            data: Optional[WeatherDataInput] = None) -> List[CityDataType]:
        user = await engine.find_one(UserModel, UserModel.id == ObjectId(user_id))
        
        if not user:
            raise Exception("User not found")
        favorite_city_data = cache.get(city)
        
        if favorite_city_data:
            favorite_city_data = json.loads(favorite_city_data)
        
            weather_data = [WeatherDataModel(date_time=data["date_time"], 
                                             temperature=data["temperature"], 
                                             humidity=data["humidity"]) for data in favorite_city_data]
        elif data:
            weather_data = [WeatherDataModel(date_time=data.date_time, temperature=data.temperature, 
                                             humidity=data.humidity)]
        else:
            raise Exception("City not found in cache and no data provided")
        
        favorite_city = CityModel(name=city, weather_data=weather_data)
        
        user.favorites = user.favorites + [favorite_city]
        
        await engine.save(user)
        return  [CityDataType(name=city.name, weather_data=city.weather_data) for city in user.favorites]
    

    @strawberry.mutation
    async def remove_favorites(self, info, city:str, user_id:str) -> List[CityDataType]:
        user = await engine.find_one(UserModel, UserModel.id == ObjectId(user_id))
        
        if not user:
            raise Exception("User not found")
        if not user.favorites:
            raise Exception("User has no favorites yet")
        
        user.favorites = [city for city in user.favorites if str(city.name) != city]
        
        await engine.save(user)
        return  [CityDataType(name=city.name, weather_data=city.weather_data) for city in user.favorites]
    
    @strawberry.mutation
    async def add_user(self, info, first_name:str, last_name:str) -> strawberry.ID:
        if await engine.find_one(UserModel, UserModel.first_name == first_name):
            raise Exception(f"User {first_name} already exists")
        
        user = UserModel(first_name=first_name, last_name=last_name, favorites=[])
        await engine.save(user)
        id = strawberry.ID(user.id)
        return id


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(debug=os.environ["DEBUG_MODE"])
app.include_router(graphql_app, prefix="/graphql")

