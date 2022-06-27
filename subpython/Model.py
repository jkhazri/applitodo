from ..app import db
from sqlalchemy import Column,Integer,String
from datetime import datetime

# data base Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64) ,nullable=False ,unique=True)
    password = db.Column(db.String(256) ,nullable=False,unique=False)
    date = db.Column(db.DateTime ,default=datetime.now())
