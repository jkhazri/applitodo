import pymysql
from flask_migrate import Migrate

from flask import Flask, jsonify ,render_template ,redirect 
from flask import flash,session ,request ,url_for
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError 


# ---------- Owen Lib ------------- # 
# Form twf
from subpython.form import LoginForm , RegisterForm
# config
from subpython.config import Development
# validate lib
import subpython.validate as validate
# login required
from subpython.validate import login_required


app = Flask(__name__)
app.config.from_object(Development)

# data base config
db = SQLAlchemy(app)
Migrate = Migrate(app, db)

# session config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)
 


# Error Handler for 404 or 500
@app.errorhandler(404)
def page_not_found(e):
    return "404",404

@app.errorhandler(500)
def page_not_found(e):
    return "500",500


@login_required
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login",methods=["POST","GET"])
def login():

    # clear all session and cookie
    session.clear()
    
    # GET
    if request.method == "GET":
        form = LoginForm()
        return render_template("login.html", form  = form)

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        checkbox = request.form.get("checkbox")
        return request.form


@app.route("/register",methods=["POST","GET"])

def register():
    
    # GET
    if request.method == "GET":
        form = RegisterForm()
        return render_template("register.html",form=form)

    # POST
    if request.method == "POST":
        form = RegisterForm()
        username = request.form.get("username")
        password = request.form.get("password")
        password_re = request.form.get("password_re")





