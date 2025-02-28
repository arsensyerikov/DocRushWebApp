from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    isAvailable: bool
   
class Toys(BaseModel):
    id: int
    Maquin: str
    competition: str
    wins: bool

class Play(BaseModel):
    id: int
    basketball: str
    ball: str
    Jordan: bool

class Swim(BaseModel):
    id: int
    free: str
    fly: str
    wins: bool

class IT_courses(BaseModel):
    id: int
    HTML: str
    CSS: str
    PYTHON: bool

class Yamnovel(BaseModel):
    id: int
    people: str
    trases: str
    vutag: bool

class snow_gun(BaseModel):
    id: int
    high: int
    weith: int
    isAvailable: bool

class Mercedec(BaseModel):
    id: int
    types: str
    hours_power: int
    petrol: int

class Apple(BaseModel):
    id: int
    title: str
    types: int
    batrery: int

class Vegan(BaseModel):
    id: int
    what: str
    meat: str
    no_meal: str



@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    return {
        "id": book_id,
        "title": "gob bles america",
        "author": "thomas ",
        "isAvailable": True,
        
    }

@app.get("/Toys/{Toys_id}", response_model=Toys)
async def