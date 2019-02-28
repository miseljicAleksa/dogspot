from ma import ma
from models.user import UserModel
from models.item import ItemModel 
from schemas.item import ItemSchema 


class UserSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many = True)
    
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)


class UserLoginSchem(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many = True)
    username = ma.String(required=True)
    password = ma.String(required=True)
    class Meta:
        model = UserModel
 