from flask import Flask

from .categories_view import bp as bp_categories



def init_app(app: Flask):
    app.register_blueprint(bp_categories)
