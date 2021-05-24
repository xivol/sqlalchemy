from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Название')
    content = TextAreaField('Описание')
    price = FloatField('Цена')
    image = FileField('Изображение')
    is_featured = BooleanField('Показать на Главной')
    submit = SubmitField('Отправить')