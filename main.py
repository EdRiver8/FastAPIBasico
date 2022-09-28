from fastapi import FastAPI

app = FastAPI()

@app.get("/") # path operation decoration
def home():
  return {"Hola": "World"}

