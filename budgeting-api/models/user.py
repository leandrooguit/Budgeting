from sql_alchemy import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "name": self.login
        }

    @classmethod
    def find_user(cls, id):
        user = cls.query.filter_by(id=id).first()  # select * from user where id = $id
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()  # select * from user where login = $login
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()