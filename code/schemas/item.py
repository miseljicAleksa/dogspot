from ma import ma
from models.item import ItemModel
from models.user import UserModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("user",)
        dump_only = ("id",)
        include_fk = True
