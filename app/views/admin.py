from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from ..data import DataLoader
from .. import db


adminviews = Blueprint('adminviews',__name__)

@adminviews.route('/')
def test():
    return render_template('rec-system-test-page.html')

@adminviews.route('/transfer')
def load_to_database():
    if 'file' in request.args and 'tablename' in request.args:
        loader = DataLoader()
        df = loader.load_from_csv(request.args['file'])
        df.reset_index(drop=True, inplace=True)
        
        success = df.to_sql(request.args['tablename'], db.engine, if_exists='replace', method='multi')
        if success:
            return jsonify({'status':'success'})
        else:
            return jsonify({'status':'fail'})
    else:
        return jsonify({'message':'please provide a file name and a table name'})

# 127.0.0.1:5000/admin/transfer?file=id_table.csv
        
