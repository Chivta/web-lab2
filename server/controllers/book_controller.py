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
        book.title = request.form['title']
        book.author = request.form['author']
        book.publication_year = request.form.get('publication_year', None)
        book.description = request.form['description']
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book.list_books'))
    return render_template('books/form.html', form_action=url_for('book.update_book'), book=book)


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