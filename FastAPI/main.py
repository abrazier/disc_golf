from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GolferBase(BaseModel):
    name: str


class GolferModel(GolferBase):
    id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    event_name: str


class EventModel(EventBase):
    id: int

    class Config:
        orm_mode = True


class EventResultsBase(BaseModel):
    event_name: str
    name: str
    score: int


class EventResultsModel(EventResultsBase):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


@app.post("/golfer/", response_model=GolferModel)
async def create_golfer(golfer: GolferBase, db: db_dependency):
    db_golfer = models.Golfer(**golfer.dict())
    db.add(db_golfer)
    db.commit()
    db.refresh(db_golfer)
    return db_golfer


@app.get("/golfer/", response_model=List[GolferModel])
async def read_golfers(db: db_dependency):
    all_golfers = db.query(models.Golfer).all()
    return all_golfers


@app.post("/event/", response_model=EventModel)
async def create_event(event: EventBase, db: db_dependency):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/event/", response_model=List[EventModel])
async def read_events(db: db_dependency):
    all_events = db.query(models.Event).all()
    return all_events


@app.post("/event_result/", response_model=EventResultsModel)
async def create_event_result(event_results: EventResultsBase, db: db_dependency):
    db_event_result = models.EventResults(**event_results.dict())
    db.add(db_event_result)
    db.commit()
    db.refresh(db_event_result)
    return db_event_result


@app.get("/event_result/", response_model=List[EventResultsModel])
async def read_events_results(db: db_dependency):
    all_event_results = db.query(models.EventResults).all()
    return all_event_results
