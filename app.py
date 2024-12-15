from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

# My app
app = Flask(__name__)





@app.route('/')
def index(): # Home main page
    return render_template("index.html")





if __name__ in "__main__":
    app.run(debug=True)