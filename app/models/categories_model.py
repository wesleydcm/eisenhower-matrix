from dataclasses import dataclass, field

from app.configs.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Text


@dataclass
class Categories(db.Model):

    id: int
    name: str
    description: str
    tasks: list = field(default_factory=list)

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    