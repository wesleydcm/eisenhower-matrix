from app.models.categories_model import Categories
import psycopg2
from app.exceptions.TasksErrors import InvalidTaskClassificationError
from app.models.eisenhowers_model import Eisenhowers
from app.models.tasks_model import Tasks
from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, InvalidRequestError


def create_task():
    try:
        data = request.json
        
        eisenhower_id = Tasks.verify_eisenhower_classification(data)

        data['eisenhower_id'] = eisenhower_id

        categories = data['categories']

        del data['categories']

        print(categories)
        print(data)

        new_task: Tasks = Tasks(**data)

        for ctg in categories:
            print(ctg['name'])
            x: Categories = Categories.query.filter_by(name=ctg['name']).first()
            if not x:
                x: Categories = Categories(name=ctg['name'])
            
            new_task.category.append(x)


        session = current_app.db.session
        session.add(new_task)
        session.commit()

        return jsonify(new_task), 201


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


def update_task():
    ...


def delete_task():
    ...
