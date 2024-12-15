from flask_sqlalchemy import SQLAlchemy
from .task_model import db


# Data Class
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Tag {self.name}"