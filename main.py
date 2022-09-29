# pertenece a python como tal
from enum import Enum

# antes que fastapi, porque este trabaja con pydantic (gerarquia)
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
  white = "White"
  brown = "Brown"
  black = "Black"
  red = "Red"
  blonde = "Blonde"

class Person(BaseModel):
  first_name: str = Field(
    ..., 
    min_length=1, 
    max_length=50
    )
  last_name: str = Field(
    ..., 
    min_length=1, 
    max_length=50
    )
  age: int = Field(
    ...,
    le=115,
    gt=0    
  )
  hair_color: HairColor | None = Field(default=None)
  is_married: bool | None = Field(default=None)
  
  class Config:
    schema_extra = {
      "example":{
        "first_name":"Edw",
        "last_name":"River",
        "age":"36",
        "hair_color":"Blonde",
        "is_married": False
      }
    }
  
class Location(BaseModel):
  city: str = Field(example="Med")
  state: str = Field(example="Antoquia")
  country: str = Field(example="Colombia")
  

@app.get("/") # path operation decoration
def home():
  return {"Hola": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)): # '...' significan que el parametro 'Body' es obligatorio
  return person


#Validaciones: Query Parameters

@app.get("/person/detail") # minimo 1, maximo 50
def show_person(
  name: str | None = Query(
    default=None, 
    alias="name-query", 
    min_length=1, 
    max_length=50,
    description="This is the person name. Its between 1 and 50 characters",
    example="Kate"
    ),
  age: str = Query(
    ..., 
    title="Person Age",
    example="22"
    )
): 
  return {name: age}


#Validaciones: Path Parameters; en este no se usa max o min, sino gt, le

@app.get("/person/detail/{person_id}")
def show_person(
  person_id: int = Path(
    ..., 
    gt=0,
    example="123"
    )
):
  return {person_id: "It exists!"}


#Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
  person_id: int = Path(
    ...,
    title="Person ID",
    description="This is the person ID",
    gt=0,
    example="123"
    ),
  person: Person = Body(...),
  location: Location = Body(...)
):
  results = person.dict() # uniendo los dos bodys de dif models
  results.update(location)
  return person;

# Con un solo request body, para que la subclase 'Config' de person funcione, swagger no funciona
# @app.put("/person/{person_id}")
# def update_person(
#   person_id: int = Path(
#     ...,
#     title="Person ID",
#     description="This is the person ID",
#     gt=0
#     ),
#   person: Person = Body(...)
# ):
#   return person;