from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email
from wtforms import ValidationError
from app.models import User

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(), Length(min=1,max=64),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8,max=40)])
    remember_me=BooleanField()
    submit=SubmitField("Login")

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("Account does not exist yet. Create a new account")
