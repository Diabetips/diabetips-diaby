import argparse
import os

from App.ClientDiabetipsApi.ApiService import ServiceDiabetipsApi
from App.IA.BasicModel import BasicModel
from App.IA.TensorModel import TensorModel


class CommandDispatcher(object):
    apiService = ServiceDiabetipsApi()

    def __init__(self, model):
        self.modelManager = model
        return

    def get_user(self, id):
        user = self.apiService.user.get(id)
        if user.status_code != 200:
            raise Exception("Unknown user")
        return user

    def build(self, id):
        user = self.get_user(id).json()
        try:
            model = self.modelManager.create_model(user)
        except:
            raise Exception("Error while creating the model")
        try:
            self.modelManager.save_model(model, user)
        except:
            raise Exception("Error while Saving the model")
        return

    def train(self, id):
        user = self.get_user(id).json()
        try:
            model = self.modelManager.load_model(user)
        except:
            raise Exception("Error while loading the model")
        try:
            self.modelManager.train_model(model, user)
        except:
            raise Exception("Error while Training the model")
        self.modelManager.save_model(model, user)
        return

    def evaluate(self, id):
        user = self.get_user(id).json()
        try:
            model, insulin = self.modelManager.load_model(user)
        except:
            raise Exception("Error while loading the model")
        res = self.modelManager.evaluate_model(model, user)
        res.append(insulin)
        return res


def main():
    parser = argparse.ArgumentParser(description='Manage user models')
    parser.add_argument('--model_type', dest='model', action='store_const', default="Basic")
    parser.add_argument('--uuid', type=str, help='Uuid of the user to treat', required=True)

    parser.add_argument('--build', dest='build', action='store_const', default=None)
    parser.add_argument('--train', dest='train', action='store_const', default=None)
    parser.add_argument('--evaluate', dest='evaluate', action='store_const', default=None)

    args = parser.parse_args()
    cd = CommandDispatcher(TensorModel() if args.model == "Tensor" else BasicModel())
    if args.build:
        cd.build(args.uuid)
    if args.train:
        cd.train(args.uuid)
    if args.evaluate:
        cd.evaluate(args.uuid)


if __name__ == "__main__":
    main()
