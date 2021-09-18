from flask import render_template, redirect, url_for, flash, request, \
    current_app, abort
from flask_login import current_user, login_required
from app import db
from app.models import Book
from app.main import bp
from app.main.forms import EmptyForm, UpdateInventoryForm, AddBookForm, \
    SearchForm
from sqlalchemy import or_


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    book = Book.query.order_by(Book.id).paginate(
        page, current_app.config['BOOKS_PER_PAGE'], False)
    next_url = url_for('main.index', page=book.next_num) \
            if book.has_next else None
    prev_url = url_for('main.index', page=book.prev_num) \
            if book.has_prev else None
    if current_user.username != 'admin':
        form = EmptyForm()
    else:
        form = UpdateInventoryForm()    
    if form.validate_on_submit():
        db.session.commit()      
    return render_template('index.html', title='Home', 
            form=form, user=current_user, book=book.items, next_url=next_url,
            prev_url=prev_url)


@bp.route('/update_inventory/<bookname>', methods=['GET', 'POST'])
@login_required
def update_inventory(bookname):
    book = Book.query.filter_by(bookname=bookname).first()
    form = UpdateInventoryForm()
    if form.validate_on_submit():
        book.update_inventory(form.inventory.data)
        db.session.commit()    
        return redirect(url_for('main.index'))
    return render_template('book.html', title=bookname, user=current_user,
                form=form, book=book)


@bp.route('/user')
@login_required
def user():
    book = current_user.books_issued
    form = EmptyForm()
    return render_template('index.html', title='MyBooks', user=current_user,
            form=form, book=book)


@bp.route('/issue/<bookname>', methods=['POST'])
@login_required
def issue(bookname):
    book = Book.query.filter_by(bookname=bookname).first()
    form = EmptyForm()
    if current_user.issue_book(book):
        db.session.commit()
        flash(f'Book {bookname} issued')
    else:
        abort(400)              
    return redirect(url_for('main.index'))


@bp.route('/return/<bookname>', methods=['POST'])
@login_required
def returnn(bookname):
    book = Book.query.filter_by(bookname=bookname).first()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.return_book(book)
        db.session.commit()   
        flash(f'Book {bookname} returned')
    return redirect(url_for('main.index'))


@bp.route('/add_book', methods=['GET','POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(bookname=form.bookname.data, author=form.author.data, 
                inventory=form.inventory.data)
        db.session.add(book)
        db.session.commit()
        flash(f'Congratulations, book {book.bookname} added to database')
        return redirect(url_for('main.index'))
    return render_template('addBook.html', title='AddBook', form=form)


@bp.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    results = None
    if form.validate_on_submit():
        search_value = form.search_string.data
        search = "%{0}%".format(search_value)
        results = Book.query.filter(or_(Book.bookname.like(search),
                Book.author.like(search))).all()
    return render_template('search.html', title='Search', user=current_user, 
            form=form, book=results)


@bp.route('/<bookname>')
@login_required
def book(bookname):
    book = Book.query.filter_by(bookname=bookname).first()
    if current_user.username != 'admin':
        form = EmptyForm()
    else:
        form = UpdateInventoryForm()
    if book:    
        return render_template('book.html', title=bookname, user=current_user,
                form=form, book=book)
    else:
        abort(400)                           