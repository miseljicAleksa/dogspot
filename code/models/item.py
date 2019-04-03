from typing import List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)

    gender = db.Column(db.String(80))
    description = db.Column(db.String(320))
    age = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()