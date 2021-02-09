from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

class MakePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), 
                                            Length(min=2, max=-1)])
    body = StringField('Body', widget=TextArea())
    submit = SubmitField('Make post')