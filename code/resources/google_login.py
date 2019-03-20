from flask_restful import Resource
from oa import google


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        return google.authorize(callback="http://localhost:5000/login/google/authorized")
