#This file has the models related to the user
from interface import db, bcrypt, login_manager
from flask_login import UserMixin

#This is the user loader to be able to use the login_manager extension
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#This is the users model in accordance to the mysql table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    is_admin = db.Column(db.Boolean)
    profile_desc = db.Column(db.String(length=200))
    profile_pic = db.Column(db.String(length=50))
    score = db.Column(db.Integer())

    #These are used to hash and unhash the password for better security
    @property
    def unhashed_password(self):
        return self.unhashed_password

    @unhashed_password.setter
    def unhashed_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    #This checks the password when logging in
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
