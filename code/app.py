import os
 
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager #in deep
from flask_cors import CORS
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout #01101010
from resources.item import Item, ItemList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET

app = Flask(__name__)

load_dotenv(".env", verbose=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

patch_request_class(app, 10 * 1024 * 1024) # 10mb max
configure_uploads(app, IMAGE_SET)

api = Api(app)
migrate = Migrate(app, db)
cors = CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


# this method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)
