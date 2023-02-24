![](https://img.shields.io/badge/fastapi-v0.92.0-brightgreen)
![](https://img.shields.io/badge/GraphQL-v3.3-blue)
# congenial-weatherman
A simple weather forcasting app build with FastAP, Strawberry, ODMantic and Mongodb

## Getting started
You will need `python 3.10` and above to run this app

Install or update pip `pip install --upgrade pip`

install virtualenv `pip install virtualenv` or install `miniconda` to isolate your python evironment

Create an python evironment using virtualenv `virtualenv -p python3 venv` (venv is the name of your environment and you can named it anything)

Or if you like to use miniconda create an environment like this `conda create -n venv`

Activate your env `source venv/bin/activate`

Install `docker` [here](https://docs.docker.com/get-docker/)

Start docker 

## Run
To launch the app run `make start`

## Testing

run `pytest tests` 

go to `http://localhost:8000/graphql` run some queries and mutations

## GraphQL Queries 
* query weather by city, date and time. 
Use date format utc "YYYY-MM-DD HH:MM:SS"
Forcast date must be within 5 days of current date 
```
query getWeather {
  getWeatherByCity(cityName: "Los Angeles", date: "2023-02-24 00:00:00") {
    name
    weatherData {
      dateTime
      humidity
      temperature
    }
  }
}
```

* Get a user favorites weather data by user id, 
user_id is obtain during user creation
```
query getFavs {
  getFavorites(userId:"63f862cc0065fab44d366aa9") {
    name
    weatherData{
      dateTime
      temperature
      humidity
    }
  }
}
```

* Check if a city's weather info exist
```
query getCity {
  getCityData (cityName: "Seattle") {
    name
    weatherData{
      dateTime
      temperature
      humidity
    }
  }
}
```

* Query a user by user_id. 
```
query user {
  getUser (firstName: "Elon", userId: "63f862cc0065fab44d366aa9") {
     id
    firstName
    lastName
  }
}
```

## GraphQL Mutations
* create a user
```
mutation myMutation{
 addUser(firstName:"Elon", lastName: "Monk") 
}
```
* add favorite 
```
mutation addFavs {
  addFavorites(city:"Los Angeles", userId: "63f862cc0065fab44d366aa9") {
    name
   weatherData {
    dateTime
    temperature
    humidity
  	}
  }
}
```
* delete favorite
```
mutation deleteFav {
  removeFavorites(city:"Seattle", userId:"63f862cc0065fab44d366aa9") {
    name
    weatherData{
      dateTime
    }
  }
}
```
