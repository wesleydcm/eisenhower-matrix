from flask import Blueprint
from app.controllers.categories_controller import create_category, delete_category, list_categories, update_category

bp = Blueprint('categories', __name__)


bp.post('/categories')(create_category)
bp.patch('/category/<int:id>')(update_category)
bp.delete('/category/<int:id>')(delete_category)
bp.get('/')(list_categories)