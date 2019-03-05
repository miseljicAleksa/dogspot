from ma import ma
from models.user import UserModel
from models.item import ItemModel 
from schemas.item import ItemSchema 

from marshmallow import Schema, fields, pre_dump


class UserSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many = True)
    
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "activated")

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user        