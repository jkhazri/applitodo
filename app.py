from datetime import datetime

from flask import Flask, jsonify ,render_template ,redirect 
from flask import flash,session ,request ,url_for
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError 
from flask_sqlalchemy import SQLAlchemy


# ---------- Owen Lib ------------- # 
from subpython.validate import login_required
from subpython.form import LoginForm , RegisterForm
from subpython.config import Development
import subpython.validate as validate



app = Flask(__name__)
app.config.from_object(Development)

# data base config
db = SQLAlchemy(app)


# session config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)
 

# USers Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64) ,nullable=False ,unique=True)
    password = db.Column(db.String(256) ,nullable=False,unique=False)
    date = db.Column(db.DateTime ,default=datetime.now())

# Tasks Model
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    task_title = db.Column(db.String(32) ,nullable=False ,unique=True)
    task_info = db.Column(db.String(128) ,nullable=False,unique=False)
    status = db.Column(db.Integer ,default=0)
    # 0 = on Doing || 1 = Done!
    date = db.Column(db.DateTime ,default=datetime.now())


# Error Handler for 404 or 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return "500",500


@app.route("/")
@login_required
def index():
    if session.get("user_id"):
        return render_template("index.html")
    return redirect("login")


@app.route("/login",methods=["POST","GET"])
def login():

    # clear all session and cookie
    session.clear()
    
    form = LoginForm()
    # GET
    if request.method == "GET":
        return render_template("login.html", form=form,error=False)

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        checkbox = request.form.get("checkbox")

        # safety check
        if not validate.validate_field(username):
            return render_template("login.html", form=form,error=True,error_message="Username is invalid :(")
        if not validate.validate_field(password):
            return render_template("login.html", form=form,error=True,error_message="Password is invalid :(")
            

        # check username and password
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template("login.html", form=form,error=True,error_message="information Wrong :(")
        
        if user.username != username:
            return render_template("login.html", form=form,error=True,error_message="username is Wrong :(")

        pass_db = user.password
        if not check_password_hash(pass_db,password):
            return render_template("login.html", form=form,error=True,error_message="Password is Wrong :(")
        
        session["user_id"] = user.id
        flash(f"Welcome dear {user.username} ")
        return redirect("/")



@app.route("/register",methods=["POST","GET"])
def register():
    
    # GET
    if request.method == "GET":
            form = RegisterForm()
            return render_template("register.html",form=form,error=False)

    # POST
    if request.method == "POST":
        form = RegisterForm()
        username = request.form.get("username")
        password = request.form.get("password")
        password_re = request.form.get("password_re")

        # safety check            
        if not username:
            return render_template("register.html",error=True,error_message="Username is Invalid")
        if not password or not password_re or password != password_re:
            return render_template("register.html",error=True,error_message="Passwords Not Match")

        # check user is not duplicated
        user_check = User.query.filter_by(username=username).first()
        if user_check:
            return render_template("register.html",form=form,error=True,error_message="Username Already Take by Another User")



        # add it ro to data base
        new_user = User(username=username,password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash(f"Register complete {username} :) ")
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")