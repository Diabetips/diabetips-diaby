from datetime import datetime, timezone

from flask import Flask
from flask_restful import Resource, Api

from App.ApiService.Pagination import Pagination
from App.ApiService.Users import ServiceDiabetipsApi

app = Flask(__name__)
api = Api(app)
backApiService = ServiceDiabetipsApi()

class Predict(Resource):

    def get(self, user_id):
        min = datetime.now(timezone.utc).timestamp() - 10800
        max = datetime.now(timezone.utc).timestamp()
        page = Pagination(100, 1, start=min, end=max)
        backApiService.user.get(user_id, page)
        meals = []
        meals = backApiService.meals.get_all(user_id, page).json()
        insulins = backApiService.insulin.get_all(user_id, page).json()
        backApiService.blood_glucose.get_all(user_id, page)
        glucose = sum(map(lambda meal: float(meal['total_sugar']) * 30, meals))
#        print("Glucose", glucose)
        insulineRes = glucose / 15
#        print("insulineRes", insulineRes)
        totalInsu = sum(map(lambda insulin: float(0 if insulin['type'] == 'slow' else int(insulin['quantity']) * ((max - min) / (int(insulin['timestamp']) - min))), insulins))
#        print("totalInsu", totalInsu)
        insulineRes -= totalInsu
        if (insulineRes < 0):
            return {'result': int(0)}
#        print("insulineRes", insulineRes)
        return {'result': int(insulineRes)}


api.add_resource(Predict, '/models/<string:user_id>/predict')

if __name__ == '__main__':
    app.run(debug=True)
