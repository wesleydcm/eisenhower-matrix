from flask import Flask

from .categories_view import bp as bp_categories
from .tasks_view import bp as bp_tasks



def init_app(app: Flask):
    app.register_blueprint(bp_categories)
    app.register_blueprint(bp_tasks)
