from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(512), nullable=False)
    author = Column(String(256), default="")
    subject = Column(String(256), default="")
    year = Column(Integer, nullable=True)
    abstract = Column(Text, default="")
    tags = Column(String(512), default="")
    availability = Column(String(16), default="available")  # available/unavailable

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(128), index=True)
    item_id = Column(Integer, index=True)
    action = Column(String(32))  # click/borrow/like
    ts = Column(DateTime(timezone=True), server_default=func.now())
