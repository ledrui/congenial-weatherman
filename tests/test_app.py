from fastapi.testclient import TestClient
import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/graphql")
    assert response.status_code == 200


# account zuck 
# id: 63f83d109a3ef78b373d019d
# first_name: Iliass
# id: 63f83d109a3ef78b373d019d
# account Elons
# id: 63f862cc0065fab44d366aa9

