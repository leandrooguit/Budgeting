from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from resources.budgeting import Budgetings, Budgeting
from resources.user import User, UserRegister, UserLogin, UserLogout


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "DontTellAnyone"
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def new_database():
    db.create_all()


@jwt.token_in_blacklist_loader
def verifier_blacklist(token):
    return token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def access_token_invalidated():
    return jsonify({"message": "You have been logged out."}), 401  # Unauthorized


api.add_resource(Budgetings, "/budgetings")
api.add_resource(Budgeting, "/budgetings/<int:id>")
api.add_resource(User, "/users/<int:id>")
api.add_resource(UserRegister, "/registrations")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)


# referencia

# localhost
# http://127.0.0.1:5000/budgetings

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://pypi.org/project/flask-restful-swagger-3/
# https://docs.sqlalchemy.org/en/13/core/defaults.html

# https://www.treinaweb.com.br/blog/o-que-e-flask/
# https://www.treinaweb.com.br/blog/django-ou-flask-eis-a-questao/
# https://blog.hallanmedeiros.com/2011/11/23/sql-paginando-resultados-com-limit-e-offset/

# documentacao
# https://readthedocs.org/projects/flask-restful-doc/downloads/pdf/stable/
# https://github.com/Sean-Bradley/Seans-Python3-Flask-Rest-Boilerplate


# https://itnext.io/postman-vs-insomnia-comparing-the-api-testing-tools-4f12099275c1
# https://www.youtube.com/watch?v=iZ2Tah3IxQc
