from flak_wtf import FlaskForm,StringField,SubmitField
from wtf.validators import DataRequired,Length

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Submit")