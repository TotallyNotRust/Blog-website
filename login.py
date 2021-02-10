from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    password = StringField('Password', validators=[DataRequired(), 
                                                  Length(min=1)])
    submit = SubmitField('Submit')