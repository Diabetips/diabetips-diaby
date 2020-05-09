from random import random

import flask
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Predict(Resource):
    def get(self, user_id):
        return {'result': 12}


api.add_resource(Predict, '/models/<string:user_id>/predict')

if __name__ == '__main__':
    app.run(debug=True)
