from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My app
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Data Class
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    isCompleted = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"


# Routes
@app.route('/')
def index(): # Home main page
    return render_template("index.html")





if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)