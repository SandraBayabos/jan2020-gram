from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from config import Config


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="images")
    image = pw.CharField(null=True, default=None)

    @hybrid_property
    def user_image(self):
        return f"{Config.AWS_LINK}/{self.image}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
