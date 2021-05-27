from flask_wtf import FlaskForm
from wtforms import *


class DeleteForm(FlaskForm):
    id = HiddenField('Id')
    confirm = SubmitField('Удалить')
    cancel = SubmitField('Отменить')