from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_rented = BooleanField("Арендован")
    arendator_id = StringField('Арендатор')
    condition = StringField('Состояние')
    submit = SubmitField('Применить')

