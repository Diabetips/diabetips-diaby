import requests

baseUrl = "https://api.diabetips.fr/v1"
usersUrl = baseUrl + "/users"

class ServiceDiabetipsApi:

    def __init__(self):
        self.Connection()

    def Get(self, url):
        return requests.get(url)

    def Connection(self):
        return

    def GetUser(self, id):
        return self.Get(usersUrl + "/" + id)


