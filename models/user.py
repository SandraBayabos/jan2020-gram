from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    usernname = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)

    def validate(self):
        duplicate_user = User.get_or_none(User.usernname == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_user:
            self.errors.append("That name is taken.")
        elif duplicate_email:
            sels.errors.append("An account with that email already exists.")
