from models.service import ServiceModel
from typing import List
from sql_alchemy import db


class CloudModel(db.Model):
    __tablename__ = "cloud"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cloudProviderEnum = db.Column(db.String(30))
    region = db.Column(db.String(255))
    zone = db.Column(db.String(255))
    amount = db.Column(db.Float(precision=2))
    services = db.relationship("ServiceModel", cascade="all")

    def __init__(self, cloudProviderEnum, region, zone, amount, services: List[ServiceModel]):
        self.cloudProviderEnum = cloudProviderEnum
        self.region = region
        self.zone = zone
        self.amount = amount
        self.services = services

    def json(self):
        return {
            "id": self.id,
            "cloudProviderEnum": self.cloudProviderEnum,
            "region": self.region,
            "zone": self.zone,
            "amount": self.amount,
            "services": [service.json() for service in self.services]
        }