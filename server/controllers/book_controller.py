from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.models import db, Book

book_bp = Blueprint('book', __name__, url_prefix='/books')


@book_bp.route('/')
def list_books():
    books = db.session.execute(db.select(Book)).scalars().all()
    return render_template('books/list.html', books=books)


@book_bp.route('/<int:book_id>')
def view_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.list_books'))
    return render_template('books/view.html', book=book)


@book_bp.route('/create', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form.get('publication_year', None)  # Use get() to avoid KeyError
        description = request.form['description']

        # Перевіряємо, чи існує вже книга з такою назвою та автором
        existing_book = Book.query.filter_by(title=title, author=author).first()

        if existing_book:
            errors = {'title': 'A book with this title and author already exists!'}
            return render_template('books/form.html', form_action=url_for('book.create_book'), title=title, author=author,
                               publication_year=publication_year, description=description, errors=errors)

        new_book = Book(title=title, author=author, publication_year=publication_year, description=description)
        db.session.add(new_book)
        db.session.commit()
        flash('Book created successfully!', 'success')
        return redirect(url_for('book.list_books'))
    return render_template('books/form.html', form_action=url_for('book.create_book'))


@book_bp.route('/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.list_books'))


    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form.get('publication_year', None)
        description = request.form['description']


        # Перевіряємо, чи існує вже інша книга з такою назвою та автором (крім поточної)
        existing_book = Book.query.filter_by(title=title, author=author).filter(Book.id != book_id).first()


        if existing_book:
            errors = {'title': 'A book with this title and author already exists!'}
            return render_template('books/form.html', form_action=url_for('book.update_book', book_id=book_id), book=book, errors=errors)


        book.title = title
        book.author = author
        book.publication_year = publication_year
        book.description = description
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book.list_books'))
    return render_template('books/form.html', form_action=url_for('book.update_book', book_id=book_id), book=book)

@book_bp.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found!', 'danger')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    return redirect(url_for('book.list_books'))