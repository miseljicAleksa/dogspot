from ma import ma
from models.user import UserModel
from models.item import ItemModel 
from schemas.item import ItemSchema 

from marshmallow import Schema, fields


class UserSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many = True)
    
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)


class UserLoginSchema(Schema):
    password = fields.Str(required=True)
    username = fields.Str(required=True)

