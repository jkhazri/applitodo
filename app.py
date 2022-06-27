import pymysql
from datetime import datetime

from flask import Flask, jsonify ,render_template ,redirect 
from flask import flash,session ,request ,url_for
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError 


# ---------- Owen Lib ------------- # 
from subpython.form import LoginForm , RegisterForm
from subpython.config import Development
import subpython.validate as validate
from subpython.validate import login_required

app = Flask(__name__)

# app config 
app.config.from_object(Development)
# data base config
db = SQLAlchemy(app)

# session config
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def remember_me(status):
    if status == True:
        app.config["SESSION_PERMANENT"] = True
    else:
        app.config["SESSION_PERMANENT"] = False



# data base Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64) ,nullable=False ,unique=True)
    password = db.Column(db.String(256) ,nullable=False)
    date = db.Column(db.DateTime ,default=datetime.now())



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
        
        # safety check
        if not validate.validate_field(username):
            return render_template("register.html", form=form,error=True,error_message="Username is Wring :(")
        if not validate.validate_passwords(password,password_re):
            return render_template("register.html", form=form,error=True,error_message="Passwords is Wrong :(")

        # see user duplicate in data base
        
        try:
            res = User.query.filter(User.username == username)
            if not res:
                return render_template("register.html", form=form,error=True,error_message="User Already take by Another User :(")
            # add user to data base
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.flush()
            db.session.rollback()
            return render_template("register.html",form=form ,error=True ,error_message="User Already take by Another User :(")


        flash("Register is complete :)")
        return redirect("login")




