from datetime import datetime

from flask import Flask, jsonify ,render_template ,redirect 
from flask import flash,session ,request ,url_for
from flask_session import Session
import sqlalchemy

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError 
from flask_sqlalchemy import SQLAlchemy


# ---------- Owen Lib ------------- # 
from subpython.validate import login_required
from subpython.form import LoginForm , RegisterForm
from subpython.config import Development,Production
import subpython.validate as validate



app = Flask(__name__)
app.config.from_object(Production)

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
    new_user = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime ,default=datetime.now())

# Tasks Model
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    task_title = db.Column(db.String(64) ,nullable=False ,unique=False)
    task_info = db.Column(db.String(256) ,nullable=False,unique=False)
    status = db.Column(db.Integer ,default=0)
    # 0 = on Doing || 1 = Done!
    date = db.Column(db.DateTime ,default=datetime.now())


# Error Handler for 404 or 500
@app.errorhandler(500)
def error_500_server(e):
    return "500",500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
@login_required
def index():
    if session.get("user_id"):
        # get user all task from data base
        user_db_data = Task.query.filter_by(user_id=(session['user_id'])).all()
        print(len(user_db_data))
        return render_template("index.html",user_db=user_db_data,user_id=session['user_id'])
    else:
        return redirect("login")


@app.route("/login",methods=["POST","GET"])
def login():

    if request.method == "GET":
        session.clear()
        form_login = LoginForm()
        return render_template("login.html", form=form_login,error=False)

    # POST
    if request.method == "POST":
        form_login = LoginForm(request.form)
        if form_login.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            checkbox = request.form.get("checkbox")
            
            # safety check
            if not validate.validate_field(username):
                return render_template("login.html", form = form_login ,error=True,error_message="Username is invalid :(")
            if not validate.validate_field(password):
                return render_template("login.html", form = form_login ,error=True,error_message="Password is invalid :(")
                

            # check username and password
            user = User.query.filter_by(username=username).first()
            if not user:
                return render_template("login.html", form=form_login,error=True,error_message="information Wrong :(")
            
            if user.username != username:
                return render_template("login.html", form=form_login,error=True,error_message="username is Wrong :(")

            pass_db = user.password
            if not check_password_hash(pass_db,password):
                return render_template("login.html", form=form_login,error=True,error_message="Password is Wrong :(")
            
            # add user id in db to user session
            session["user_id"] = user.id

            # check its first time user log in to web site to show welcome message
            if user.new_user == 0:
                user.new_user = 1
                db.session.commit()

                flash(f"{user.username}")
                first = validate.first_login
                return redirect('/')
            else:
                return redirect("/")
        
        else:
             return render_template("login.html", form=form_login,error=True, error_message="Invalid Inputs")



@app.route("/register",methods=["POST","GET"])
def register():
    
    # GET
    if request.method == "GET":
            form = RegisterForm()
            return render_template("register.html",form=form,error=False)

    # POST
    if request.method == "POST":
        form = RegisterForm(request.form)
        if form.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            password_re = request.form.get("password_re")

            # safety check            
            if not validate.validate_field(username):
                return render_template("register.html",form=form,error=True,error_message="Username Is invalid :(")
            
            password_validation = validate.validate_passwords(password,password_re)
            if password_validation == "NS":
                return render_template("register.html",form=form,error=True,error_message="Passwords Are Not Match :(")
            elif password_validation == False:
                return render_template("register.html",form=form,error=True,error_message="Passwords are Wrong")


            # check user is not duplicated
            user_check = User.query.filter_by(username=username).first()
            if user_check:
                return render_template("register.html",form=form,error=True,error_message="Username Already Take by Another User")

            # add it ro to data base 
            new_user = User(username=username,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            # query to data base
            user_in_db = User.query.filter_by(username=username).first()
            if not user_in_db:
                return error_500_server()

            # add first column(welcome message too user task column)
            new_task = Task(user_id=user_in_db.id,task_title=validate.first_login[1],task_info=validate.first_login[2])
            db.session.add(new_task)
            db.session.commit()

            flash(f"Register complete {username} :) ")
            return redirect('login')
        else:
            return render_template("register.html",form=form,error=True,error_message="Invalid Inputs :(")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/edit",methods=["POST","GET"])
def edit():
    return render_template("edit.html",post_id=request.form.get("task"))


@app.route("/delete")
def delete():
    return render_template("delete.html",post_id=request.form.get('task'))


@app.route("/add_new_task",methods=['POST'])
def add_new_task():
    title = request.form.get("Task_Info")
    info = request.form.get("Task_Name")   

    if not validate.validate_tasks(title):
        return redirect('/')
    if not validate.validate_tasks(info):
        return redirect('/')
    

    # add task to user db
    new_task = Task(user_id=session['user_id'],task_info=info,task_title=title)
    try:
        db.session.add(new_task)
        db.session.commit()
    except:
        return error_500_server()
    return redirect('/')




@app.route("/action_target", methods=["POST"])
def action_target():
    action = request.form.get("action")
    
    # edit section
    if action.lower() == "edit":
        title = request.form.get("Edit_Task_Name")
        info = request.form.get("Edit_Task_Info")
        task_id = request.form.get("task")

        if not validate.validate_tasks(title):
            return redirect('/')
        if not validate.validate_tasks(info):
            return redirect('/')
        
        try:
            new_task = Task.query.filter_by(id=task_id).first()
            if not new_task:
                return redirect("/")

            new_task.task_title=title
            new_task.task_info=info
            db.session.commit()
        except:
            return error_500_server
        
        return redirect("/")

    # delete section
    elif action.lower() == "delete":
        pass
    
    else:
        return redirect("/")
    



@app.route("/middle_center", methods=["POST"])
def middle_center():
    if request.form.get("action") == "edit":
        return redirect("edit")
    if request.form.get("action") == "delete":
        return "delete"
    if request.form.get("action") == "done":
        return "done"