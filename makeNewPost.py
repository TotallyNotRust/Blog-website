from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class MakePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), 
                                            Length(min=2, max=-1)])
    body = StringField('Body', widget=TextArea())
    pictures = FileField('File', validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Make post')