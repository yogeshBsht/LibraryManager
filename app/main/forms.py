from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')  


class UpdateInventoryForm(FlaskForm):
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    submit = SubmitField(('Update'))