from flask_restful import Resource, reqparse
from app.data import DataLoader
import os
import json
from flask import jsonify, make_response, Blueprint
from collections import OrderedDict
from app.models.beta_recommender import BetaRecommender
from app.models.preparation import us_news_data_cleaner
from flask_restful import request as rest_rq


api_bp = Blueprint('api',__name__)

class USNewsRequest(Resource):

    def __init__(self):
        self.loader = DataLoader()
        df = self.loader.load_from_csv('us_news_2023.csv')
        self.reqparse = reqparse.RequestParser()

        for col_name in df.columns:
            self.reqparse.add_argument(col_name, default='')
        # self.reqparse.add_argument('id', type=str, default='')
        # self.reqparse.add_argument('name', type=str, default='')
        # self.reqparse.add_argument('address', type=str, default='')
        # self.reqparse.add_argument('age', type=str, default='')

    def get(self):
        args = self.reqparse.parse_args()
        args = {k: v for k, v in args.items() if v}
        conditions = {k: args[k] for k in args.keys()}
        df = self.loader.get_rows_from_csv('us_news_2022.csv',conditions)
        data = {}
        for index, row in df.iterrows():
            data[index] = self.loader.serialize_row(row, df.columns)

        out = {'content-type':'text/json'}
        payload = data
        out['data'] = payload

        return jsonify(out)

    def put(self):
        pass

    def post(self):
        pass


class BetaRecommend(Resource):

    def __init__(self):
        self.loader = DataLoader()
        df = self.loader.load_from_csv('us_news_2022.csv')
        self.reqparse = reqparse.RequestParser()

        for col_name in df.columns:
            self.reqparse.add_argument(col_name, default='')

    def get(self):
        out = {}
        out['status'] = 405
        out['message'] = 'GET method not allowed, please use POST method to access this endpoint.'

        return make_response(jsonify(out),405)

    def post(self):
        id = rest_rq.form.get('id')
        rec_engine = BetaRecommender(self.loader.load_from_csv('us_news_2022.csv').copy())

        rec_engine.set_features(id_col='id', features=['name', 'rankingType',
                                                       'urlName', 'fundingType', 'location',
                                                        'percentReceivingAid', 'hsGpa'], drop=True)

        rec_engine.clean_data(us_news_data_cleaner)

        result_df = rec_engine.run(id)
        original_df = self.loader.load_from_csv('us_news_2022.csv')

        result_data = {}
        i=0
        for index, row in result_df.iterrows():
            result_data[i] = self.loader.serialize_row(row, result_df.columns)
            i+=1

        out = {'content-type':'text/json'}
        payload = {}
        input_df = self.loader.get_rows_from_csv('us_news_2022.csv',{'id':id})
        input_data = input_df.loc[0].to_dict()
        payload['search_input'] = self.loader.serialize_row(input_data, input_df.columns)
        payload['results'] = result_data
        out['data'] = payload


        return make_response(jsonify(out), 200)

class Search(Resource):
    def get(self): # partial name -> list of {id, name, location}
        args = self.reqparse.parse_args()
        raw_input = args['input']

        out = {}
        out['status'] = 405
        out['message'] = 'GET method not allowed, please use POST method to access this endpoint.'

        return make_response(jsonify(out),405)


class FullRecommend(Resource):
    def get(self):
        out = {}
        out['status'] = 405
        out['message'] = 'GET method not allowed, please use POST method to access this endpoint.'

        return make_response(jsonify(out),405)
    
    def post(self):
        pass #TODO implement after constructing ML model
