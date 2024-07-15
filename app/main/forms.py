from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Submit")