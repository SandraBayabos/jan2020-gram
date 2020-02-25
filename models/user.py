from models.base_model import BaseModel
import peewee as pw
import re


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)

    def validate(self):
        duplicate_user = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        # password length check
        if len(self.password) < 6:
            self.errors.append("Password must be at least 6 characters")

        if not re.search(r"\d", self.password):
            self.errors.append("Password must contain digit")

        if duplicate_user:
            self.errors.append("That name is taken.")

        if duplicate_email:
            self.errors.append("An account with that email already exists.")

    # @classmethod
    # def validate_password(self, password):
    #     valid_password = True
    #     while not valid_password:
    #         reg = "(?=.*[a-z])"

    #         # compiling regex
    #         pat = re.compile(reg)

    #         # searching regex
    #         mat = re.search(pat, password)

    #         # validating conditions
    #         if mat:
    #             valid_password = True
    #         else:
    #             self.errors.append("Password invalid!")
    #             valid_password = False

    #     return valid_password
