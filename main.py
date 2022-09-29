# pertenece a python como tal
from typing import Optional

# antes que fastapi, porque este trabaja con pydantic (gerarquia)
from pydantic import BaseModel

from fastapi import FastAPI, Body

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
