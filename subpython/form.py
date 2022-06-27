from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField , BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,email_validator


# user name 6- 64
# password - 10 - 64256


# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username" ,validators=[DataRequired(),
                                        Length(min=6,max=64) ])
    password = PasswordField("Password" ,validators=[DataRequired(),
                                        Length(min=6,max=256)])

    # remember = BooleanField("Remember ME")
    submit = SubmitField("Login")


# REgister Form
class RegisterForm(FlaskForm):
    username = StringField("Username" ,validators=[DataRequired(),
    Length(min=6,max=64)])

    password = PasswordField("Password" ,validators=[DataRequired()
     ,Length(min=6,max=256)])

    password_re = PasswordField("Confirmation Password" ,validators=[DataRequired()
     ,Length(min=6,max=256) ,EqualTo('password', message="Passwords Must Be match")])
    
    submit = SubmitField("Register")