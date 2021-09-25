import psycopg2
import sqlalchemy
from app.models.categories_model import Categories
from flask import current_app, jsonify, request
from sqlalchemy import exc
from sqlalchemy.sql.coercions import expect


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

    except sqlalchemy.exc.IntegrityError as e:
        print(e.orig)

        # Campo faltando
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'msg': str(e.orig).split('\n')[0]}, 400

        # Campo unico já existe
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {'msg': str(e.orig).split('\n')[1]}, 422
