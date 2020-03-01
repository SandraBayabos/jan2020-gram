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
