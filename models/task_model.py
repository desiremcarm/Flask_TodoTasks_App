from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Data Class
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(120))
    isCompleted = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', backref='tasks')

    def __repr__(self) -> str:
        return f"Task {self.id}"