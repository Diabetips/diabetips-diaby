from App.ClientDiabetipsApi.Pagination import Pagination
from App.ClientDiabetipsApi.ApiService import ServiceDiabetipsApi
from datetime import datetime, timezone

from App.IA.AModel import AModel


class BasicModel(AModel):
    usersDirectory = "UserDatas"
    backApiService = ServiceDiabetipsApi()

    def create_model(self, user_data):
        return None

    def save_model(self, model, user_data):
        return None

    def train_model(self, model, user_data):
        pass

    def load_model(self, user_data):
        return None

    def evaluate_model(self, model, user_data):
        user_id = user_data['uid']
        min = datetime.now(timezone.utc).timestamp() - 10800
        max = datetime.now(timezone.utc).timestamp()
        page = Pagination(100, 1, start=min, end=max)
        self.backApiService.user.get(user_id, page)
        meals = self.backApiService.meals.get_all(user_id, page).json()
        insulins = self.backApiService.insulin.get_all(user_id, page).json()
        self.backApiService.blood_glucose.get_all(user_id, page)
        glucose = sum(map(lambda meal: float(meal['total_sugar']) * 20, meals))
        #        print("Glucose", glucose)
        insulineRes = glucose / 15
        #        print("insulineRes", insulineRes)
        totalInsu = sum(map(lambda insulin: float(0 if insulin['type'] == 'slow' else int(insulin['quantity']) * (
                    (max - min) / (int(insulin['timestamp']) - min))), insulins))
        #        print("totalInsu", totalInsu)
        insulineRes -= totalInsu
        if (insulineRes < 0):
            return {'result': int(0)}
        return {'result': int(insulineRes)}
