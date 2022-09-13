from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_restful import Api, Resource
from flask_migrate import Migrate
from app.api.api import FullRecommend, Search, USNewsRequest, BetaRecommend
import os
from dotenv import load_dotenv



db = SQLAlchemy()
DB_NAME = "database.db"
ENV_PATH = os.path.join(os.getcwd(), '..','.env')

API_NAV = "/api/"

app = Flask(__name__)  # intialize flask app

def create_app():
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # I love python! 256
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
    app.config['JSON_SORT_KEYS'] = False


    db.init_app(app)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # create local db, if not already exists
    # will be disabled in production
    # create_local_db(app)

    db.create_all(app=app)

    


    # set up API here
    api = create_api(app)
    api.add_resource(USNewsRequest,API_NAV+'usnews2022/')
    api.add_resource(BetaRecommend,API_NAV+'usnews2022/recommend/')
    api.add_resource(Search, API_NAV+'search/')
    api.add_resource(FullRecommend, API_NAV+'recommend/')

    # set up views here
    from .views.admin import adminviews
    from .api.api import api_bp

    app.register_blueprint(adminviews, url_prefix='/admin/')
    app.register_blueprint(api_bp)

    return app

def create_api(app):
    return Api(app)

def create_local_db(app):
    if not os.path.exists('app'+os.sep+DB_NAME):
        db.create_all(app=app)
    return db


app = create_app()