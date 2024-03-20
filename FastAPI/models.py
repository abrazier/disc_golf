from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class Golfer(Base):
    __tablename__ = "golfers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)


class EventResults(Base):
    __tablename__ = "event_results"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    name = Column(String)
    score = Column(Integer)
    name_id = Column(String, ForeignKey("golfers.id"))
