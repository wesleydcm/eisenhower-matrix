from flask import Blueprint
from app.controllers.categories_controller import create_category

bp = Blueprint('categories', __name__, url_prefix='/categories')


bp.post('')(create_category)