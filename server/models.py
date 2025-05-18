from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)
    description = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    favorite_books = db.relationship('Book', secondary='user_book_subscription', backref=db.backref('users', lazy=True))


user_book_subscription = db.Table('user_book_subscription',
                               db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                               db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                               db.Column('date_added', db.DateTime, nullable=False))