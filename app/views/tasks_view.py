from flask import Blueprint
from app.controllers.tasks_controller import create_task, delete_task, update_task

bp = Blueprint('tasks', __name__, url_prefix="/task")


bp.post('')(create_task)
bp.patch('/<int:id>')(update_task)
bp.delete('/<int:id>')(delete_task)
