import unittest
from app import create_app, db
from app.models import User, Book
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='guest')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_set_superuser(self):
        u1 = User(username='admin', superuser=1)
        u2 = User(username='guest')
        u1.set_superuser()
        u2.set_superuser()
        self.assertTrue(u1.superuser)
        self.assertFalse(u2.superuser)
    
    def test_issue(self):
        u = User(username='guest')
        b1 = Book(bookname='book1', inventory=2)
        b2 = Book(bookname='book2', inventory=0)
        db.session.add(u)
        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()
        self.assertFalse(u.has_issued(b1))
        self.assertFalse(u.has_issued(b2))
        self.assertEqual(u.books_issued.count(),0)

        u.issue_book(b1)
        u.issue_book(b2)
        db.session.commit()
        self.assertTrue(u.has_issued(b1))
        self.assertEqual(u.books_issued.count(),1)
        self.assertFalse(u.has_issued(b2))

        u.return_book(b1)
        db.session.commit()
        self.assertFalse(u.has_issued(b1))
        self.assertEqual(u.books_issued.count(),0)


class BookModelCase(unittest.TestCase):  
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_update_inventory(self):    
        b1 = Book(bookname='book1', inventory=2)
        b1.update_inventory(3)
        self.assertTrue(b1.inventory==3)
        self.assertFalse(b1.inventory==2)


if __name__ == '__main__':
    unittest.main(verbosity=2)