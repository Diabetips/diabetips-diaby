
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

from App.Error.InternalError import InternalError
from App.IA.BasicModel import BasicModel

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('from')

class Predict(Resource):
    model = BasicModel()

    def get(self, user_id):
        args = parser.parse_args()
#        print("insulineRes", insulineRes)
        model = self.model.create_model(user_id)
        self.model.train_model(model, user_id)
        try:
            res = self.model.evaluate_model(model, user_id, args['from'])
        except InternalError as error:
            return {'message': error.message, 'error_code': error.status_code}, error.status_code
        return res


api.add_resource(Predict, '/models/<string:user_id>/predict')

if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(InternalError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response