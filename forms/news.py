from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок')
    content = TextAreaField('Текст')
    image = FileField('Изображение')
    is_featured = BooleanField('Показать на Главной')
    submit = SubmitField('Отправить')