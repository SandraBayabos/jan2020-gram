from models.base_model import BaseModel
from flask import url_for
import peewee as pw
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property, hybrid_method
from config import Config


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)
    user_profile_image = pw.CharField(null=True, default=False)
    public = pw.BooleanField(default=True)

    def validate(self):
        existing_username = User.get_or_none(User.username == self.username)
        existing_email = User.get_or_none(User.email == self.email)

        if existing_username and not existing_username.id:
            self.errors.append("That name is taken.")

        if existing_email and not existing_email.id:
            self.errors.append("An account with that email already exists.")

        # password length check
        if not self.id and len(self.password) < 6:
            self.errors.append("Password must be at least 6 characters")

        if not self.id and not re.search(r"\d", self.password):
            self.errors.append("Password must contain digit")
        else:
            if not self.id:
                self.password = generate_password_hash(self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @hybrid_property
    def profile_image(self):
        if self.user_profile_image:
            return f"{Config.AWS_LINK}/{self.user_profile_image}"
        else:
            return url_for("static", filename="images/default.jpg")

    @hybrid_property
    def is_private(self):
        if not self.public:
            return False

    @hybrid_property
    def followers(self):
        from models.follower_following import FollowerFollowing
        return [user.idol for user in FollowerFollowing.select().where(FollowerFollowing.fan_id == self.id)]

    @hybrid_property
    def following(self):
        from models.follower_following import FollowerFollowing
        return [user.fan for user in FollowerFollowing.select().where(FollowerFollowing.idol_id == self.id)]

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.fan_id == user.id) & (FollowerFollowing.idol_id == self.id)) else False

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
