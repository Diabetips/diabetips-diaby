from App.ClientDiabetipsApi.ApiService import ServiceDiabetipsApi


class AModel(object):
    backApiService = ServiceDiabetipsApi()

    def __init__(self):
        pass

    def create_model(self, user_id):
        return None

    def save_model(self, model, user_data):
        return None

    def train_model(self, model, user_data):
        pass

    def load_model(self, userData):
        return None

    def evaluate_model(self, model, user_data):
        return None
