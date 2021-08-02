from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Book
from app.main import bp
from app.main.forms import EmptyForm, UpdateInventoryForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    book = Book.query.all()
    form = EmptyForm()
    if form.validate_on_submit():
        db.session.commit()  
    return render_template('index.html', title='Home', form=form, user=current_user, book=book)


# @bp.route('/update_inventory', methods=['GET', 'POST'])
# @login_required
# def update_inventory():
#     book = Book.query.all()
#     form = UpdateInventoryForm()
#     if form.validate_on_submit():
#         # current_user.issue_book(book)
#         db.session.commit()    
#     return render_template('index.html', form=form, user=current_user, book=book)


@bp.route('/user')
@login_required
def user():
    book = current_user.books_issued
    form = EmptyForm()
    return render_template('index.html', title='MyBooks', user=current_user, form=form, book=book)


@bp.route('/issue/<bookname>', methods=['POST'])
@login_required
def issue(bookname):
    form = EmptyForm()
    book = Book.query.filter_by(bookname=bookname).first()
    if form.validate_on_submit():
        current_user.issue_book(book)
        db.session.commit()        
    return redirect(url_for('main.index'))


@bp.route('/return/<bookname>', methods=['POST'])
@login_required
def returnn(bookname):
    form = EmptyForm()
    book = Book.query.filter_by(bookname=bookname).first()
    if form.validate_on_submit():
        current_user.return_book(book)
        db.session.commit()   
    return redirect(url_for('main.index'))