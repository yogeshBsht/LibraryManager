from flask import render_template, redirect, url_for, flash, request, \
    current_app, abort, g
from flask_login import current_user, login_required
from app import db
from app.models import Book
from app.main import bp
from app.main.forms import EmptyForm, UpdateInventoryForm, AddBookForm, \
    SearchForm
from sqlalchemy import or_


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home', 
            user=current_user)


@bp.route('/update_inventory/<bookname>', methods=['GET', 'POST'])
@login_required
def update_inventory(bookname):
    book = Book.query.filter_by(bookname=bookname).first()
    form = UpdateInventoryForm()
    if form.validate_on_submit():
        book.update_inventory(form.inventory.data)
        db.session.commit()
        flash(f'Congratulations, book {book.bookname} inventory updated \
            to {form.inventory.data}')    
        return redirect(url_for('main.index'))
    return render_template('book.html', title=bookname, user=current_user,
                form=form, book=book)


@bp.route('/user')
@login_required
def user():
    book = current_user.books_issued.all()
    for b in book:
        print(b.bookname)
    form = EmptyForm()
    return render_template('search.html', title='MyBooks', user=current_user,
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
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    if current_user.username != 'admin':
        form = EmptyForm()
    else:
        form = UpdateInventoryForm()    
    page = request.args.get('page', 1, type=int)
    book, total = Book.search(g.search_form.q.data, page,
                               current_app.config['BOOKS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['BOOKS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', user=current_user, 
            form=form, book=book, next_url=next_url, prev_url=prev_url)


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