from dataclasses import asdict

import psycopg2
from app.exceptions.TasksErrors import InvalidTaskClassificationError
from app.models.categories_model import Categories
from app.models.tasks_model import Tasks
from flask import current_app, jsonify, request
from sqlalchemy.exc import (IntegrityError, InvalidRequestError,
                            ProgrammingError)


def create_task():
    try:
        data = request.json
        
        eisenhower_id = Tasks.verify_eisenhower_classification(data)

        data['eisenhower_id'] = eisenhower_id

        categories = data['categories']

        del data['categories']

        new_task: Tasks = Tasks(**data)
        
        category_list = list()


        for ctg in categories:
            x: Categories = Categories.query.filter_by(name=ctg['name']).first()
            if not x:
                x: Categories = Categories(name=ctg['name'])
            
            new_task.category.append(x)
            category_list.append({"name": x.name})


        session = current_app.db.session
        session.add(new_task)
        session.commit()


        task = asdict(new_task)
        task['category'] = category_list


        return task, 201


    except KeyError as e:
        return {"msg": f'Need to have property {str(e)}'}, 400
    
    except ValueError as e:
        return {"msg": str(e)}, 400
    
    except InvalidTaskClassificationError as error:
        return jsonify({'error': error.message}), 404
    
    except IntegrityError as e:
        print(e.orig)

        # Campo faltando
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'msg': str(e.orig).split('\n')[0]}, 400

        # Campo unico já existe
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {'msg': str(e.orig).split('\n')[1]}, 409


def update_task(id: int):

    task: Tasks = Tasks.query.get(id)
    print(task.importance)

    if not task:
        return {"msg": "task not found!"}, 404


    try:
        data = request.json

        Tasks.query.filter_by(id=id).update(data)

        task: Tasks = Tasks.query.get(id)

        update_eisenhower_classification = {
        'importance': task.importance,
        'urgency': task.urgency
        }

        eisenhower_id = Tasks.verify_eisenhower_classification(update_eisenhower_classification)

        data['eisenhower_id'] = eisenhower_id

        Tasks.query.filter_by(id=id).update(data)

        task: Tasks = Tasks.query.get(id)

        session = current_app.db.session
        session.commit()

        return jsonify(task), 200

    except ProgrammingError as e:
        if type(e.orig) == psycopg2.errors.SyntaxError:
            return jsonify({"msg": "Sintax error"}), 404

    # Campo não existe
    except TypeError as e:
        return jsonify({"msg": str(e)}), 400

    except IntegrityError as e:
        print(e.orig)

        # Campo faltando
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'msg': str(e.orig).split('\n')[0]}, 400

        # Campo unico já existe
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {'msg': str(e.orig).split('\n')[1]}, 409
    
    except InvalidRequestError as e:
        return jsonify({"msg": str(e)}), 400


def delete_task(id: int):
    task = Tasks.query.get(id)

    if not task:
        return jsonify({"msg": "task not found!"}), 404

    session = current_app.db.session
    session.delete(task)
    session.commit()

    return jsonify(''), 204
