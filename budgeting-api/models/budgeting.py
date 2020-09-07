from typing import List
import sqlalchemy
from models.microservice import MicroServiceModel
from sql_alchemy import db


class BudgetingModel(db.Model):
    __tablename__ = "budgeting"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    totalCost = db.Column(db.Float(precision=2))
    periodEnum = db.Column(db.String(10))
    currencyEnum = db.Column(db.String(6))
    effectiveFrom = db.Column(db.Date())
    effectiveTo = db.Column(db.Date())
    description = db.Column(db.String(255))
    paymentTypeEnum = db.Column(db.String(10))
    microServices = db.relationship("MicroServiceModel", cascade="all")
    running = db.Column(db.String(3), default="NO")
    creation = db.Column(db.Date(), server_default=sqlalchemy.sql.func.now())

    def __init__(self, name, totalCost, periodEnum, currencyEnum, effectiveFrom, effectiveTo, description,
                 paymentTypeEnum, microServices: List[MicroServiceModel]):
        self.name = name
        self.totalCost = totalCost
        self.periodEnum = periodEnum
        self.currencyEnum = currencyEnum
        self.effectiveFrom = effectiveFrom
        self.effectiveTo = effectiveTo
        self.description = description
        self.paymentTypeEnum = paymentTypeEnum
        self.microServices = microServices

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "totalCost": self.totalCost,
            "periodEnum": self.periodEnum,
            "currencyEnum": self.currencyEnum,
            "effectiveFrom": str(self.effectiveFrom),
            "effectiveTo": str(self.effectiveTo),
            "description": self.description,
            "paymentTypeEnum": self.paymentTypeEnum,
            "running": self.running,
            "creation": str(self.creation),
            "microServices": [microService.json() for microService in self.microServices]
        }

    @classmethod
    def find_budgeting(cls, id):
        budgeting = cls.query.filter_by(id=id).first()  # select * from budgeting where id = $id
        if budgeting:
            return budgeting
        return None

    @classmethod
    def find_by_running_scenario(cls):
        budgeting = cls.query.filter_by(running="YES").first()  # select * from budgeting where running = YES
        if budgeting:
            return budgeting
        return None

    def save_budgeting(self):
        db.session.add(self)
        db.session.commit()

    def update_scenario_budgeting(self, running):
        self.running = running

    def delete_budgeting(self):
        db.session.delete(self)
        db.session.commit()