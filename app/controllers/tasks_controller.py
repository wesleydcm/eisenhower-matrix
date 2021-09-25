import psycopg2
from app.exceptions.tasks_exp import InvalidTaskValueError
from app.models.eisenhowers_model import Eisenhowers
from app.models.tasks_model import Tasks
from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, InvalidRequestError


def verify_eisenhower_classification(importance: int, urgency: int):
    if importance != 1 and importance != 2:
        raise InvalidTaskValueError("importance needs integer equal 1 or 2")            
    elif urgency != 1 and urgency != 2:
        raise InvalidTaskValueError("urgency needs integer equal 1 or 2")


    do_it_first: Eisenhowers = Eisenhowers.query.filter_by(type='Do It First').first()
    delegate_it: Eisenhowers = Eisenhowers.query.filter_by(type='Delegate It').first()
    schedule_it: Eisenhowers = Eisenhowers.query.filter_by(type='Schedule It').first()
    delete_it: Eisenhowers = Eisenhowers.query.filter_by(type='Delete It').first()


    if not do_it_first:
        session = current_app.db.session
        
        session.add(Eisenhowers(type='Do It First'))
        session.add(Eisenhowers(type='Delegate It'))
        session.add(Eisenhowers(type='Schedule It'))
        session.add(Eisenhowers(type='Delete It'))

        session.commit()


    if importance == 1 and urgency == 1:
        return do_it_first.type
    if importance == 1 and urgency == 2:
        return delegate_it.type
    if importance == 2 and urgency == 1:
        return schedule_it.type

    return delete_it.type



def create_task():
    try:
        data = request.json

        importance: int = int(data["importance"])
        urgency: int = int(data["urgency"])

        eisenhower_classification = verify_eisenhower_classification(importance, urgency)

        

        return jsonify({"eisenhower_classification": eisenhower_classification}), 200

    except KeyError as e:
        return {"msg": f'Need to have property {str(e)}'}, 400
    
    except ValueError as e:
        return {"msg": str(e)}, 400
    
    except InvalidTaskValueError as e:
        return {"msg": str(e)}, 400

def update_task():
    ...


def delete_task():
    ...
