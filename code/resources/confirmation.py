from time import time
import traceback

from flask import make_response, render_template
from flask_restful import Resource

from models.confirmation import ConfirmationModel
from models.user import UserModel
from resources.user import USER_NOT_FOUND
from schemas.confirmation import ConfirmationSchema
from libs.mailgun import MailgunException


NOT_FOUND = "Confirmation reference not found."
EXPIRED = "The link has expired."
ALREADY_CONFIRMED = "Registration has already been confirmed."
RESEND_FAIL = "Internam server error, failed to resend conf email"
RESEND_SUCCESSFUL = "email conf successfully resent"

confirmation_schema = ConfirmationSchema()

class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
           return {"message": ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type":"text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email), 200, headers)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        
        return (
            {
                "current-time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )


    @classmethod
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": ALREADY_CONFIRMED}, 400
                confirmation.force_to_expire()
            
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": RESEND_SUCCESSFUL}, 201

        except MailgunException as e:
            return {"message": e.message}, 500
        except:
            traceback.print_exc()
            return {"message": RESEND_FAIL}, 500