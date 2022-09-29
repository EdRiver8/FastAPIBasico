# pertenece a python como tal
from typing_extensions import Required

# antes que fastapi, porque este trabaja con pydantic (gerarquia)
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models
class Person(BaseModel):
  first_name: str
  last_name: str
  age: int
  hair_color: str | None = Field(default=None, example="Blonde, Dark")
  is_married: bool | None = None
  
class Location(BaseModel):
  city: str
  state: str
  country: str
  

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
    description="This is the person name. Its between 1 and 50 characters"
    ),
  age: str = Query(
    ..., 
    title="Person Age"
    )
): 
  return {name: age}


#Validaciones: Path Parameters; en este no se usa max o min, sino gt, le

@app.get("/person/detail/{person_id}")
def show_person(
  person_id: int = Path(
    ..., 
    gt=0
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
    gt=0
    ),
  person: Person = Body(...),
  location: Location = Body(...)
):
  results = person.dict() # uniendo los dos bodys de dif models
  results.update(location)
  return person;