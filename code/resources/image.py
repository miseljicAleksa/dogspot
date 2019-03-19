from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()


IMAGE_UPLOADED = "Image successfully uploaded"
IMAGE_ILLEGAL_EXTENSION = "You have to upload image with legal extension"
IMAGE_ILLEGAL_FILENAME = "Your filename is illegal"
IMAGE_NOT_FOUND = "Image not found"
IMAGE_DELETED = "Image deleted successfully"
IMAGE_DELETED_FAILED = "Failed to delete image"
AVATAR_DELETED_FAILED = "Failed to delete avatar"
AVATAR_UPLOADED = "Avatar successfully uploaded"
AVATAR_NOT_FOUND = "Avatar not found"

class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = image_schema.load(request.files) # {"image" : FileStorage}
        user_id = get_jwt_identity()
        folder = "user_{}".format(user_id)
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": IMAGE_UPLOADED}, 201
        
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": IMAGE_ILLEGAL_EXTENSION}, 400


class Image(Resource):
    @classmethod
    @jwt_required
    def get(cls, filename: str):
        user_id = get_jwt_identity()
        folder = "user_{}".format(user_id)
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME}, 400
        try:
            return send_file(image_helper.get_path(filename, folder=folder)) 
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND}, 404 
    @classmethod
    def delete(cls, filename: str):
        user_id = get_jwt_identity()
        folder = "user_{}".format(user_id)
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME}
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": IMAGE_DELETED}, 200
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND}, 404
        except:
            traceback.print_exc()
            return {"message": IMAGE_DELETED_FAILED}, 500

class AvatarUpload(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        data = image_schema.load(request.files)
        filename = "user_{}".format(get_jwt_identity())
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": AVATAR_DELETED_FAILED}, 500
            
        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(data["image"], folder=folder, name=avatar)
            basename = image_helper.get_basename(avatar_path)
            return {"message": AVATAR_UPLOADED}, 200
        
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": IMAGE_ILLEGAL_EXTENSION}, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        folder = "avatars"
        filename = "user_{}".format(user_id)
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar: 
            return send_file(avatar)
        return {"message": AVATAR_NOT_FOUND}, 404