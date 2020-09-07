from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt

from blacklist import BLACKLIST
from models.user import UserModel

args = reqparse.RequestParser()
args.add_argument("login", type=str, required=True, help="The field 'login' cannot be left blank.")
args.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank.")


class User(Resource):
    def get(self, id):
        user = UserModel.find_user(id)
        if user:
            return user.json()
        return {"message": "User not found."}, 404  # http status not found

    @jwt_required
    def delete(self, id):
        user = UserModel.find_user(id)
        if user is None:
            return {"message": "User not found."}, 404  # http status not found

        try:
            user.delete_user()
        except:
            return {"message": "An error ocurred trying to delete user."}, 500  # Internal Server Error

        return {"message": "User deleted."}, 204  # no content


class UserRegister(Resource):
    def post(self):
        data = args.parse_args()

        if UserModel.find_by_login(data["login"]):
            return {"message": "The login '{}' already exists.".format(data["login"])}, 400  # Bad request

        user = UserModel(**data)

        try:
            user.save_user()
        except:
            return {"message": "An internal error ocurred trying to save user."}, 500  # Internal Server Error

        return {"message": "User created successfully!"}, 201  # Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()

        user = UserModel.find_by_login(data["login"])

        if user and safe_str_cmp(user.password, data["password"]):
            acsess_token = create_access_token(identity=user.id)
            return {"acsess_token": acsess_token}, 201  # Created

        return {"message": "The username or password is incorrect."}, 401  # Unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()["jti"]  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully!"}, 200  # status code OK
