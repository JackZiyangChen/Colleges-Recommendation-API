from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from app.api.api import USNewsRequest, BetaRecommend



db = SQLAlchemy()
DB_NAME = "database.db"

API_NAV = "/api/"

def create_app():
    app = Flask(__name__)  # intialize flask app
    app.config['SECRET_KEY'] = "c3a845a318cd654749ea4db6f4d5f9cb5c6e5b0cade46d9dc04af46d32049c7c"  # I love python! 256
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JSON_SORT_KEYS'] = False
    db.init_app(app)


    # set up API here
    api = create_api(app)
    api.add_resource(USNewsRequest,API_NAV+'usnews2022/')
    api.add_resource(BetaRecommend,API_NAV+'usnews2022/recommend/')

    # set up views here
    from .views.admin import adminviews
    from .api.api import api_bp

    app.register_blueprint(adminviews, url_prefix='/admin/')
    app.register_blueprint(api_bp)

    return app

def create_api(app):
    return Api(app)

