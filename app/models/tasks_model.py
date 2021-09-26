from app.models.tasks_categories_table import tasks_categories
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.TasksErrors import InvalidTaskClassificationError
from app.models.categories_model import Categories
from app.models.eisenhowers_model import Eisenhowers
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.schema import ForeignKey


@dataclass
class Tasks(db.Model):

    id: int
    name: str
    description: str
    duration: int
    eisenhower_classification: Eisenhowers
    category: Categories


    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey('eisenhowers.id'), nullable=False)

    eisenhower_classification = relationship("Eisenhowers", backref=backref("tasks", uselist=False))
    category = relationship('Categories', secondary=tasks_categories, backref="tasks")

    @staticmethod
    def verify_eisenhower_classification(data: dict):

        importance = data['importance']
        urgency = data['urgency']

        if (
            importance != 1 and importance != 2
        ) or (
            urgency != 1 and urgency != 2
            ):
            raise InvalidTaskClassificationError(importance, urgency)

        eisenhower_types = {
            'first_quadrant': 'Do It First',
            'second_quadrant': 'Delegate It',
            'third_quadrant': 'Schedule It',
            'fourth_quadrant': 'Delete It'
        }


        do_it_first: Eisenhowers = Eisenhowers.query.filter_by(type=eisenhower_types['first_quadrant']).first()


        if not do_it_first:
            session = db.session
            
            session.add(Eisenhowers(type='Do It First'))
            session.add(Eisenhowers(type='Delegate It'))
            session.add(Eisenhowers(type='Schedule It'))
            session.add(Eisenhowers(type='Delete It'))

            session.commit()

        if importance == 1 and urgency == 1:
            do_it_first: Eisenhowers = Eisenhowers.query.filter_by(type=eisenhower_types['first_quadrant']).first()
            return do_it_first.id
        if importance == 1 and urgency == 2:
            delegate_it: Eisenhowers = Eisenhowers.query.filter_by(type=eisenhower_types['second_quadrant']).first()
            return delegate_it.id
        if importance == 2 and urgency == 1:
            schedule_it: Eisenhowers = Eisenhowers.query.filter_by(type=eisenhower_types['third_quadrant']).first()
            return schedule_it.id

        delete_it: Eisenhowers = Eisenhowers.query.filter_by(type=eisenhower_types['fourth_quadrant']).first()

        return delete_it.id
