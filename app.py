from flask import Flask, render_template, redirect, request
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
    description = db.Column(db.String(120))
    isCompleted = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"


# Routes
@app.route('/', methods=["POST", "GET"])
def index(): # Home main page
    # Add task
    if request.method == "POST":
        current_task = request.form['title']
        new_task = Task(title=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    # See all tasks
    else:
        all_tasks = Task.query.order_by(Task.created).all()
        return render_template('index.html', all_tasks=all_tasks)




if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)