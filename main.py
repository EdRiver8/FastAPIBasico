# pertenece a python como tal
from operator import le
from typing import Optional
from typing_extensions import Required

# antes que fastapi, porque este trabaja con pydantic (gerarquia)
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Query

app = FastAPI()

# Models
class Person(BaseModel):
  first_name: str
  last_name: str
  age: int
  hair_color: str | None = Field(default=None, example="Blonde, Dark")
  is_married: bool | None = None

@app.get("/") # path operation decoration
def home():
  return {"Hola": "World"}

# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)): # '...' significan que el parametro 'Body' es obligatorio
  return person

@app.get("/person/detail") # minimo 1, maximo 50
def show_person(
  name: str | None = Query(default=None, alias="name-query", min_length=1, max_length=50),
  age: str = Query(...)
): 
  return {name: age}
  
