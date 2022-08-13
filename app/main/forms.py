from flask_wtf import FlaskForm
from flask import request
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Book


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class UpdateInventoryForm(FlaskForm):
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    submit = SubmitField(('Update'))

    def validate_inventory(self, inventory):
        if inventory.data<0:
            raise ValidationError(('Inventory must be non-negative.'))


class AddBookForm(FlaskForm):
    bookname = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    inventory = IntegerField('Inventory', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_bookname(self, bookname):
        book = Book.query.filter_by(bookname=bookname.data).first()
        if book is not None:
            raise ValidationError(('Book already exists.'))


class SearchForm(FlaskForm):
    q = StringField(('Search Books'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class ReviewForm(FlaskForm):
    rating = SelectField('Rate the book', choices=[1, 2, 3, 4, 5], coerce=int, validate_choice=True)
    body = TextAreaField(('Write your review here.'), validators=[DataRequired()])
    submit = SubmitField(('Submit'))