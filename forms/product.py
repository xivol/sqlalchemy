from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data.categories import Categories


class ProductForm(FlaskForm):
    title = StringField('Название')
    content = TextAreaField('Описание')
    price = FloatField('Цена')
    image = FileField('Изображение')
    is_featured = BooleanField('Показать на Главной')
    categories = FieldList(BooleanField('Категория'))
    submit = SubmitField('Отправить')

    def __init__(self, db_sess):
        super().__init__()
        categories = db_sess.query(Categories)
        for cat in categories:
            self.categories.append_entry(False)
            self.categories[-1].label.text = cat.title