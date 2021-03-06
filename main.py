
#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Chimbote"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Santa"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Peru"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example= "Miguel"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config: 
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "Garcia Martoni",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }

@app.get('/')
def home():
    return {"Hello": "World"}

# Request and Response body

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person


#Validaciones: Query Parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1,
        max_length=50,
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
    ),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required",
        example=25
    )
):
    return {name: age}

# Validaciones path parameters

@app.get('/person/detail/{person_id}')
def show_person_detail(
    person_id: int = Path(
        ..., 
        gt=0,
        title='Person Id',
        description="This is the person id. It's required",
        example=123
    )
):
    return { person_id: 'It exists!' }

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="This is the person Id",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

