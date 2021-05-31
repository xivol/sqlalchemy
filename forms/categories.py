from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CategoriesForm(FlaskForm):
    title = StringField('Название')
    content = TextAreaField('Описание')
    submit = SubmitField('Отправить')