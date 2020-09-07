from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from models.budgeting import BudgetingModel
from models.microservice import MicroServiceModel
from models.cloud import CloudModel
from models.service import ServiceModel
from typing import List
from datetime import date
from flask_jwt_extended import jwt_required


def normalize_path_params(limit=10, offset=0, **data):
    return {
        "limit": limit,
        "offset": offset
    }


path_params = reqparse.RequestParser()
path_params.add_argument("limit", type=int)
path_params.add_argument("offset", type=int)


class Budgetings(Resource):
    @jwt_required
    def get(self):
        data = path_params.parse_args()
        valid_data = {key: data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_data)

        return {"budgetings": [budgeting.json() for budgeting in
                               BudgetingModel.query.limit(params["limit"]).offset(params["offset"])]}  # select * from budgeting

    @jwt_required
    def post(self):

        def microservice_parser(microService):
            newMicroService = {
              "cloud": microService["cloud"],
              "description": microService["description"],
              "name": microService["name"]
            }
            return newMicroService

        args = reqparse.RequestParser()
        args.add_argument("currencyEnum", type=str, required=True)
        args.add_argument("description", type=str, required=True)
        args.add_argument("effectiveFrom", type=str, required=True)
        args.add_argument("effectiveTo", type=str, required=True)
        args.add_argument("microServices", type=microservice_parser, action="append", required=True)
        args.add_argument("name", type=str, required=True)
        args.add_argument("paymentTypeEnum", type=str, required=True)
        args.add_argument("periodEnum", type=str, required=True)
        args.add_argument("totalCost", type=float, required=True)

        try:
            data = args.parse_args()

            def create_services(services):
                objects: List[ServiceModel] = []
                for service in services:
                    objects.append(ServiceModel(service["name"], service["value"], service["tag"],
                                                service["instances"], service["instanceType"]))
                return objects

            def create_cloud(cloud):
                return CloudModel(cloud["cloudProviderEnum"], cloud["region"], cloud["zone"],
                                  cloud["amount"], create_services(cloud["services"]))

            def create_micro_services(microServices):
                objects: List[MicroServiceModel] = []
                for microService in microServices:
                    cloud = create_cloud(microService["cloud"])
                    microService = MicroServiceModel(microService["name"], microService["description"], cloud)
                    objects.append(microService)
                return objects

            effectiveFrom = date.fromisoformat(data["effectiveFrom"])
            effectiveTo = date.fromisoformat(data["effectiveTo"])
            budgeting = BudgetingModel(data["name"], data["totalCost"], data["periodEnum"], data["currencyEnum"],
                                       effectiveFrom, effectiveTo, data["description"], data["paymentTypeEnum"],
                                       create_micro_services(data["microServices"]))
        except KeyError:
            return {"message": "All fields of budgeting cannot be left blank."}, 400  # Bad request
        except BadRequest:
            return {"message": "All fields of budgeting cannot be left blank."}, 400  # Bad request

        try:
            budgeting.save_budgeting()
        except:
            return {"message": "An internal error ocurred trying to save budgeting."}, 500  # Internal Server Error

        return budgeting.json(), 201  # http status Created


class Budgeting(Resource):
    @jwt_required
    def get(self, id):
        budgeting = BudgetingModel.find_budgeting(id)
        if budgeting:
            return budgeting.json()
        return {"message": "Budgeting not found."}, 404  # http status not found

    @jwt_required
    def put(self, id):
        budgeting = BudgetingModel.find_budgeting(id)
        if budgeting is None:
            return {"message": "Budgeting not found."}, 404  # http status not found

        budgetingScenario = BudgetingModel.find_by_running_scenario()
        if budgetingScenario:
            running: str = "NO"
            budgetingScenario.update_scenario_budgeting(running)

        running: str = "YES"
        budgeting.update_scenario_budgeting(running)

        try:
            budgeting.save_budgeting()
        except:
            return {"message": "An internal error ocurred trying to save budgeting."}, 500  # Internal Server Error

        return budgeting.json(), 200

    @jwt_required
    def delete(self, id):
        budgeting = BudgetingModel.find_budgeting(id)
        if budgeting is None:
            return {"message": "Budgeting not found."}, 404  # http status not found

        try:
            budgeting.delete_budgeting()
        except:
            return {"message": "An error ocurred trying to delete budgeting."}, 500  # Internal Server Error

        return {"message": "Budgeting deleted."}, 204  # no content
