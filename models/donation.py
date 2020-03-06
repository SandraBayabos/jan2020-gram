from models.base_model import BaseModel
from models.image import Image
from models.user import User
from flask import url_for
import peewee as pw


class Donation(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    image = pw.ForeignKeyField(Image, backref='donations')
    user = pw.ForeignKeyField(User, backref='donations')
