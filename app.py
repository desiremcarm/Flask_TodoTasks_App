from flask import Flask, render_template, redirect, request, url_for
from flask_scss import Scss
from models.task_model import Task, db


# My ap
app = Flask(__name__)
Scss(app)


# db config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


# ROUTER

@app.route("/")
def index():
    all_tasks = Task.query.order_by(Task.created).all()
    return render_template('index.html', all_tasks=all_tasks)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        
        new_title = request.form['title']
        new_desc = request.form['description']
        new_tag = request.form['tag']
        
        new_task = Task(
            title=new_title,
            description=new_desc,
            tag=new_tag
        )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    return render_template("create.html")

# Delete task
@app.route("/del/<int:id>")
def delete(id: int):
    
    delete_task = Task.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    
    except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"


# Edit task
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id: int):
    
    update_task = Task.query.get_or_404(id)
    
    if request.method == "POST":
        
        update_task.title = request.form['title']
        update_task.tag = request.form['tag']
        update_task.description = request.form['description']
        
        try:
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    else:
        
        return render_template('edit.html', update_task=update_task)


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)