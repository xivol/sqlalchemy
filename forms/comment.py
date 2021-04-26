from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    text = StringField('Комментарий')
    submit = SubmitField('Отправить')