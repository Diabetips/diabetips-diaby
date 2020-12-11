from statistics import mean

from App.ClientDiabetipsApi.Pagination import Pagination
from App.ClientDiabetipsApi.ApiService import ServiceDiabetipsApi
from datetime import datetime, timezone

from App.Error.InternalError import InternalError
from App.IA.AModel import AModel


class BasicModel(AModel):
    usersDirectory = "UserDatas"
    backApiService = ServiceDiabetipsApi()
    gramOfSugarPerInsulinUnit = 15

    def create_model(self, user_data):
        return None

    def save_model(self, model, user_data):
        return None

    def train_model(self, model, user_data):
        pass

    def load_model(self, user_data):
        return None

    def evaluate_model(self, model, user_data, max_date):
        self.gramOfSugarPerInsulinUnit = 15
        user_id = user_data
        min_date, max_date = self.getDateInterval(max_date)
        page = Pagination(100, 1, start=min_date, end=max_date)
        user = self.backApiService.user.get(user_id, page)
        if user.status_code >= 300:
            raise InternalError("No user found", status_code=user.status_code)
        user_biometrics = self.backApiService.biometrics.get_all(user_id, page).json()
        if user_biometrics is None:
            raise InternalError('Missing user biometrics informations', status_code=404)

        self.influenceInsulinResitanceFromBMI(user_biometrics)
        self.influenceInsulinResitanceFromSex(user_biometrics)

        insulin_from_meals = self.getInsulinFromMeals(user_id, page)
        insulin_from_insulin = self.getInsulinFromInsulin(user_id, page)
        insulin_from_blood_sugar = self.getInsulinFromBloodSugar(user_biometrics, user_id, page)

        insulin_res = insulin_from_meals + insulin_from_blood_sugar - insulin_from_insulin
        if insulin_res < 0:
            return {'result': 0}
        return {'result': int(round(insulin_res))}

    def getDateInterval(self, max_date_input):
        if not max_date_input:
            max_date_input = datetime.now(timezone.utc).timestamp()
        else:
            try:
                max_date_input = self.parseDate(max_date_input).timestamp()
            except:
                raise InternalError('form : Bad format', status_code=400)
        return max_date_input - 10800, max_date_input

    def getInsulinFromInsulin(self, user_id, page):
        min_date = page.start
        max_date = page.end
        insulin_list = self.backApiService.insulin.get_all(user_id, page).json()
        insulin_total = sum(map(lambda insulin: float(0 if insulin['type'] == 'slow' else int(insulin['quantity']) * (
                    (max_date - min_date) / (self.parseDate(insulin['time']).timestamp() - min_date))), insulin_list))
        return insulin_total

    def getInsulinFromMeals(self, user_id, page):
        page.end += 60 * 20
        meals = self.backApiService.meals.get_all(user_id, page).json()
        glucose = sum(map(lambda meal: float(meal['total_carbohydrates']), meals))
        #        print("Glucose", glucose)
        insulin_total = glucose / self.gramOfSugarPerInsulinUnit
        page.end -= 60 * 20
        return insulin_total

    def getInsulinFromBloodSugar(self, user_biometrics, user_id, page):
        range_in_minute = 20
        page.start = page.end - range_in_minute * 60
        user_glucose_list = self.backApiService.blood_glucose.get_all(user_id, page).json()
        if user_biometrics['hypoglycemia'] == 0 or user_biometrics['hypoglycemia'] is None:
            raise InternalError('Missing hypoglycemia limit', status_code=404)
        if user_biometrics['hyperglycemia'] == 0 or user_biometrics['hyperglycemia'] is None:
            raise InternalError('Missing hyperglycemia limit', status_code=404)
        if user_glucose_list is None or len(user_glucose_list) == 0:
            raise InternalError('Missing recent blood sugar information', status_code=404)

        average_blood_sugar = sum(map(lambda x: x['value'], user_glucose_list)) / len(user_glucose_list)

        if average_blood_sugar <= user_biometrics['hypoglycemia']:
            return -((user_biometrics['hypoglycemia'] - average_blood_sugar) / self.gramOfSugarPerInsulinUnit)
        if average_blood_sugar >= user_biometrics['hyperglycemia']:
            return (average_blood_sugar - user_biometrics['hyperglycemia']) / self.gramOfSugarPerInsulinUnit
        return 0

    def influenceInsulinResitanceFromBMI(self, user_biometrics):
        bmi = self.getBMI(user_biometrics)
        if bmi <= 0:
            return
        if bmi > 40:
            influence = 0.5
        else:
            influence = (1 - (bmi / 40) + 0.5)
        self.gramOfSugarPerInsulinUnit *= influence

    def influenceInsulinResitanceFromSex(self, user_biometrics):
        if 'female' in user_biometrics['sex']:
            self.gramOfSugarPerInsulinUnit *= 1.1

    def getBMI(self, user_biometrics):
        if user_biometrics['height'] == 0 or user_biometrics['height'] is None:
            return 0
        if user_biometrics['mass'] == 0 or user_biometrics['mass'] is None:
            return 0
        return user_biometrics["mass"] / pow(user_biometrics["height"] / 100, 2)

    @staticmethod
    def parseDate(dateAsString):
        return datetime.strptime(dateAsString[:-5], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
