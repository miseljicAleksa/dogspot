from flask import url_for, request, session
from flask_restful import Resource
from oa import google


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        return google.authorize(callback='http://localhost:5000/oauth2callback')



class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' %(
                request.args['error_reason'],
                request.args['error_description']
            )
        session['google_token'] = (resp['access_token'], '')
        me = google.get('userinfo')  
        return me.data