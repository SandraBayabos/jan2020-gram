from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

# idols and fans are both Users. You just differentiate them with fan and idol


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")

    class Meta:
        indexes = ((('fan', 'idol'), True),)
