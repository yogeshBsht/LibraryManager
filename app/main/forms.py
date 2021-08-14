from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')  


class UpdateInventoryForm(FlaskForm):
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    submit = SubmitField(('Update'))


class AddBookForm(FlaskForm):
    bookname = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    submit = SubmitField('Add')   