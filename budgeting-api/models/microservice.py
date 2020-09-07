from sql_alchemy import db
from models.cloud import CloudModel


class MicroServiceModel(db.Model):
    __tablename__ = "micro_service"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    cloud_id = db.Column(db.Integer, db.ForeignKey("cloud.id"))
    cloud = db.relationship("CloudModel", backref="micro_service", primaryjoin="CloudModel.id==MicroServiceModel.cloud_id", uselist=False, cascade="all")

    budgeting_id = db.Column(db.Integer, db.ForeignKey('budgeting.id'), nullable=False)

    def __init__(self, name, description, cloud: CloudModel):
        self.name = name
        self.description = description
        self.cloud = cloud

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cloud": self.cloud.json()
        }