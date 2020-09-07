from sql_alchemy import db


class ServiceModel(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.Float(precision=2))
    tag = db.Column(db.String(255))
    instances = db.Column(db.String(4))
    instanceType = db.Column(db.String(255))
    cloud_id = db.Column(db.Integer, db.ForeignKey('cloud.id'), nullable=False)

    def __init__(self, name, value, tag, instances, instanceType):
        self.name = name
        self.value = value
        self.tag = tag
        self.instances = instances
        self.instanceType = instanceType

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "tag": self.tag,
            "instances": self.instances,
            "instanceType": self.instanceType
        }