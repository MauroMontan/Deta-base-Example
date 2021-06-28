from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from deta import Deta
from dotenv import load_dotenv
import os

app = FastAPI(
    debug=True
)

load_dotenv()


PROJECTKEY = os.getenv("PROJECTKEY")

deta = Deta(PROJECTKEY)


db = deta.Base("Users")


@app.post('/')
async def create(name: str, password: str):
    user = db.insert({
        "name": name,
        "password": password,
    })
    return jsonable_encoder(user)


#this function shows only one user (item), searched by name
@app.get('/')
async def readOne(name: str):
    user = next(db.fetch({"name": name}))[0]
    return jsonable_encoder(user)


#this function shows all users in database
@app.get('/showAll')
async def showAll():
    user = db.fetch()
    return jsonable_encoder(user)
