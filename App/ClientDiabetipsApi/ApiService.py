import json
import os
import random as rand
from datetime import datetime

from pip._vendor import requests

from App.ClientDiabetipsApi.Pagination import Pagination

CLIENT_ID = os.getenv('DIABETIPS_API_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DIABETIPS_API_CLIENT_SECRET')
API_URL = os.environ.get('DIABETIPS_API_URL')


class BaseServiceDiabetipsApi:



    def __init__(self):
        t = os.environ
        self.baseUrl = API_URL + "/v1"
        # grant_type = 'authorization_code'
        # body_params = {'grant_type': grant_type}
        # response = requests.post(self.baseUrl + '/auth/token', data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
        #
        # token_raw = json.loads(response.text)
        # token = token_raw["access_token"]

    def get(self, url, page: Pagination = None):
        to_search = f"{self.baseUrl}/{url}"
        if page:
            to_search += "?" + page.getRequestParameters()
        id = rand.randrange(1000, 9999)
        print(f"[GET | {id} | REQUEST] {to_search}")
        result = requests.get(to_search, timeout=10, auth=(CLIENT_ID, CLIENT_SECRET))
        print(f"[GET | {id} | RESULT] {result.json()} ")
        return result


class UserServiceDiabetipsApi(BaseServiceDiabetipsApi) :
    usersUrl = "users"

    def get(self, id, page: Pagination = None, path=""):
        return BaseServiceDiabetipsApi.get(self, self.usersUrl + "/" + id + path, page)


class UserEntryServiceDiabetipsApi(UserServiceDiabetipsApi):

    def __init__(self, _type):
        super().__init__()
        self.entryType = _type

    def get_all(self, id, page: Pagination = None):
        return UserServiceDiabetipsApi.get(self, id, page, "/" + self.entryType)


class BloodSugarServiceDiabetipsApi(UserEntryServiceDiabetipsApi):

    def __init__(self):
        UserEntryServiceDiabetipsApi.__init__(self, "blood_sugar")


class MealServiceDiabetipsApi(UserEntryServiceDiabetipsApi):

    def __init__(self):
        UserEntryServiceDiabetipsApi.__init__(self, "meals")


class InsulinServiceDiabetipsApi(UserEntryServiceDiabetipsApi):

    def __init__(self):
        UserEntryServiceDiabetipsApi.__init__(self, "insulin")

class BiometricsServiceDiabetipsApi(UserEntryServiceDiabetipsApi):

    def __init__(self):
        UserEntryServiceDiabetipsApi.__init__(self, "biometrics")


class ServiceDiabetipsApi:

    def __init__(self):
        self.user = UserServiceDiabetipsApi()
        self.blood_glucose = BloodSugarServiceDiabetipsApi()
        self.meals = MealServiceDiabetipsApi()
        self.insulin = InsulinServiceDiabetipsApi()
        self.biometrics = BiometricsServiceDiabetipsApi()

