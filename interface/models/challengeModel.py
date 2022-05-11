#This file contains the models related to challenges
from interface import db 
#This is the challenge model in accordance to the mysql table
class Challenges(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(length=20), nullable=False)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=200), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    file_url = db.Column(db.String(length=100))
    author = db.Column(db.String(length=50), nullable=False)
    flag = db.Column(db.String(length=50), nullable=False)

#This model is used to determine which challenges has each user cleared
class User_cleared_challenges(db.Model):
    user_id = db.Column(db.Integer())
    challenge_id = db.Column(db.Integer())
    __table_args__ = (
        db.PrimaryKeyConstraint(
            user_id, challenge_id,
            ),
        )