import json
import os
import random


class ModelManager(object):
    usersDirectory = "UserDatas"

    def __init__(self):
        pass

    def create_model(self, userData):
        return None

    def save_model(self, model, userData):
        return userData

    def train_model(self, model, userData):
        pass

    def load_model(self, userData):
        return None

    def evaluate_model(self, model, userData):
        return None
