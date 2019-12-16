import flask
from flask import Flask
from flask_restful import Resource, Api

from App.Models.CommandDispatcher import CommandDispatcher

app = Flask(__name__)
api = Api(app)
cd = CommandDispatcher()


class Train(Resource):
    def get(self, user_id):
        try:
            cd.train(user_id)
        except Exception as e:
            flask.abort(400, str(e))
        return {'message': 'Successfuly trained the model'}


class Build(Resource):
    def get(self, user_id):
        try:
            cd.build(user_id)
        except:
            flask.abort(400, "An error occured during the building")
        return {'message': 'Successfuly build the model'}


class Evaluate(Resource):
    def get(self, user_id):
        loss, acc = 0, 0
        try:
            loss, acc = cd.evaluate(user_id)
        except:
            flask.abort(400, "An error occured during the evaluate")
        return {'message': 'Successfuly evaluate the model', 'loss': str(loss), 'accuracy': str(acc)}


class Predict(Resource):
    def get(self, user_id):
        flask.abort(501, "Not implemented yet")


api.add_resource(Train, '/models/<string:user_id>/train')
api.add_resource(Build, '/models/<string:user_id>/build')
api.add_resource(Evaluate, '/models/<string:user_id>/evaluate')
api.add_resource(Predict, '/models/<string:user_id>/predict')

if __name__ == '__main__':
    app.run(debug=True)
