import os
from sre_constants import SUCCESS
from unicodedata import name
import json
from flask_cors import CORS
from flask import Flask, jsonify,request
from server.DS_code.Predictors.create_predictor import create_trainer
from server.DS_code.IO.get_data import create_data_fetcher_predict, create_data_fetcher_training
from flask import Flask

app = Flask(__name__)
CORS(app)

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/api/auth/register', methods = ['POST'])
def register_user():
    print(request.form)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/api/auth/login', methods = ['POST'])
def login():
    print(request.form)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/get_ges_pred',methods = ['GET'])
def get_pred():
    print("hello")
    trainer = create_trainer(create_data_fetcher_training, create_data_fetcher_predict)
    predictor = trainer()
    return str(predictor())

if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='0.0.0.0', port=8080, debug=True)
#
    # trainer = create_trainer(create_data_fetcher)
    # predictor = trainer()
    # print(predictor())

