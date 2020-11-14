import random as rand
from datetime import datetime

from pip._vendor import requests

from App.ClientDiabetipsApi.Pagination import Pagination


class BaseServiceDiabetipsApi:

    def __init__(self):
        self.baseUrl = "https://api.diabetips.fr/v1"

    def get(self, url, page: Pagination = None):
        to_search = f"{self.baseUrl}/{url}"
        if page:
            to_search += "?" + page.getRequestParameters()
        id = rand.randrange(1000, 9999)
        print(f"[GET | {id} | REQUEST] {to_search}")
        result = requests.get(to_search, timeout=10)
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


class ServiceDiabetipsApi:

    def __init__(self):
        self.user = UserServiceDiabetipsApi()
        self.blood_glucose = BloodSugarServiceDiabetipsApi()
        self.meals = MealServiceDiabetipsApi()
        self.insulin = InsulinServiceDiabetipsApi()

