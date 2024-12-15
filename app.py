from flask import Flask, render_template, redirect, request, url_for
from flask_scss import Scss
from models.tag_model import Tag
from models.task_model import Task, db

import os
import json


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
        tag_id = request.form['tag']
        
        # Find tag id
        new_tag = Tag.query.get(tag_id)
        
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
        
    # Getting all tags
    all_tags = Tag.query.all()
    return render_template("create.html", all_tags=all_tags)

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
    current_tag = update_task.tag
    
    if request.method == "POST":
        
        selected_tag_id = request.form['tag']
        selected_tag = Tag.query.get(selected_tag_id)
        
        update_task.title = request.form['title']
        update_task.description = request.form['description']
        update_task.tag = selected_tag
        
        
        print(type(selected_tag_id))
        
        
        try:
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    else:
        # Getting all tags
        all_tags = Tag.query.all()
        return render_template('edit.html', update_task=update_task, all_tags=all_tags)


# Populate db with tags data from JSON
def load_tags_from_file(file_path):
    try:
        # read json file
        with open(file_path, 'r') as file:
            data = json.load(file)
            

        # isert tags in db
        created_tags = []
        skipped_tags = []


        for item in data:

            # cehcking if the tag already exists
            existing_tag = Tag.query.filter_by(name=item['name']).first()
            if existing_tag:
                skipped_tags.append(item['name'])
                continue

            # creating new tag
            new_tag = Tag(name=item['name'], color=item['color'])
            db.session.add(new_tag)
            created_tags.append(item['name'])

        # commit to db
        db.session.commit()

    except Exception as e:
        print(f"Error loading tags: {e}")



if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'tags.json')
    
    with app.app_context():
        # Crear todas las tablas automáticamente en el orden correcto
        db.create_all()

        # Cargar los tags predeterminados
        load_tags_from_file(file_path)
    
    app.run(debug=True)
