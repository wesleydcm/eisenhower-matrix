import psycopg2
from app.models.categories_model import Categories
from app.models.tasks_model import Tasks
from app.models.tasks_categories_table import tasks_categories
from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, InvalidRequestError


def create_category():
    try:
        data = request.json

        category = Categories(**data)

        session = current_app.db.session

        session.add(category)
        session.commit()

        return jsonify(category), 201

    # Campo não existe
    except TypeError as e:
        return jsonify({"msg": str(e)}), 400

    except IntegrityError as e:

        # Campo faltando
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'msg': str(e.orig).split('\n')[0]}, 400

        # Campo unico já existe
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {'msg': str(e.orig).split('\n')[1]}, 409


def update_category(id: int):
    try:
        data = request.json

        Categories.query.filter_by(id=id).update(data)

        session = current_app.db.session
        session.commit()

        category = Categories.query.get(id)

        if not category:
            return {"msg": "category not found!"}, 404

        return jsonify(category), 200

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


def delete_category(id: int):
    category = Categories.query.get(id)
    if not category:
        return jsonify({"msg": "Category not found!"}), 404

    session = current_app.db.session
    session.delete(category)
    session.commit()

    return jsonify(''), 204


def list_categories():
    session = current_app.db.session

    query = session.query(Categories).all()

    return jsonify(query),200
