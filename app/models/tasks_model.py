from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.schema import ForeignKey


@dataclass
class Tasks(db.Model):

    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhowers_id: int


    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhowers_id = Column(Integer, ForeignKey('eisenhowers.id'), nullable=False)
