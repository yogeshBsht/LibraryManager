from flask import current_app, g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from sqlalchemy import or_


user_book = db.Table('user_book',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
    )


class Book(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(64), index=True, unique=True)
    author = db.Column(db.String(64))
    inventory = db.Column(db.Integer)

    def update_inventory(self, inventory=0):
        self.inventory = inventory

    @classmethod
    def search(cls, expression, page, per_page):
        """Search given expression in Book database and return
            results for given page and total results."""
        search = "%{0}%".format(expression)
        results = Book.query.filter(or_(Book.bookname.like(search),
                Book.author.like(search))).all()
        total = len(results)
        results = results[(page-1)*per_page:page*per_page]
        ids = [result.id for result in results]
        if total == 0:
            return None, 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total    


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

    def set_superuser(self):
        """Set superuser to False if not superuser."""
        if not self.superuser:
            self.superuser = False
    
    def has_issued(self, book):
        """Return True only if book is issued to user."""
        return self.books_issued.filter(
            user_book.c.book_id == book.id).count() == 1  

    def issue_book(self, book):
        """Issue book to user and update book inventory."""
        if not self.has_issued(book) and self.books_issued.count()<3 and book.inventory != 0:
            self.books_issued.append(book)
            book.inventory -= 1
            return 1
        return 0    

    def return_book(self, book):
        """Return book and update book inventory."""
        if self.has_issued(book):
            self.books_issued.remove(book)
            book.inventory += 1


@login.user_loader
def load_user(id):
    return User.query.get(int(id))