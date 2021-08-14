from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


user_book = db.Table('user_book',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
    )


class Book(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(64), index=True, unique=True)
    author = db.Column(db.String(64))
    inventory = db.Column(db.Integer)

    def update_inventory(self, inventory):
        self.inventory = inventory


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    superuser = db.Column(db.Boolean)
    books_issued = db.relationship(
        'Book', secondary=user_book,
        primaryjoin=(user_book.c.user_id == id),
        secondaryjoin=(user_book.c.book_id == Book.id),
        backref=db.backref('user_book', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_superuser(self):
        '''Sets superuser to False if not superuser'''
        if not self.superuser:
            self. superuser = False

    def validate_username(self, username):
        '''Raises error message if username already exists in database'''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''Raises error message if email already exists in database'''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')    
    
    def has_issued(self, book):
        '''Returns True only if a book is issued by user'''
        return self.books_issued.filter(
            user_book.c.book_id == book.id).count() == 1  

    def issue_book(self, book):
        '''Issue book to user and update book inventory'''
        if not self.has_issued(book) and self.books_issued.count()<3 and book.inventory != 0:
            self.books_issued.append(book)
            book.inventory -= 1
            print('Book issued')

    def return_book(self, book):
        '''Return book and update book inventory'''
        if self.has_issued(book):
            self.books_issued.remove(book)
            book.inventory += 1
            print('Book returned')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))