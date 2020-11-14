
from flask import Flask
from flask_restful import Resource, Api

from App.ClientDiabetipsApi.Pagination import Pagination
from App.ClientDiabetipsApi.ApiService import ServiceDiabetipsApi
from App.IA.BasicModel import BasicModel

app = Flask(__name__)
api = Api(app)

class Predict(Resource):
    model = BasicModel()

    def get(self, user_id):
#        print("insulineRes", insulineRes)
        model = self.model.create_model(user_id)
        self.model.train_model(model, user_id)
        return self.model.evaluate_model(model, user_id)


api.add_resource(Predict, '/models/<string:user_id>/predict')

if __name__ == '__main__':
    app.run(debug=True)
