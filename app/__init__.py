from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_restful import Api, Resource
from flask_migrate import Migrate
from app.api.api import FullRecommend, Search, USNewsRequest, BetaRecommend
import os



db = SQLAlchemy()
DB_NAME = "database.db"

API_NAV = "/api/"

app = Flask(__name__)  # intialize flask app

def create_app():
    app.config['SECRET_KEY'] = "c3a845a318cd654749ea4db6f4d5f9cb5c6e5b0cade46d9dc04af46d32049c7c"  # I love python! 256
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ltgyufytcurqqk:2712161adf7c052a206be5ea5bd3e9f0ae5b6de0f422250038980b6e8e4255d5@ec2-44-206-197-71.compute-1.amazonaws.com:5432/dae3ibk7serkj4'
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