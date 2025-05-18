from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.services.book_service import BookService

book_bp = Blueprint('book', __name__, url_prefix='/books')
book_service = BookService()


@book_bp.route('/')
def list_books():
    books = book_service.get_all_books()
    return render_template('books/list.html', books=books)


@book_bp.route('/<int:book_id>')
def view_book(book_id):
    book = book_service.get_book_by_id(book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.list_books'))
    return render_template('books/view.html', book=book)


@book_bp.route('/create', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form.get('publication_year', None)
        description = request.form['description']

        new_book, error_message = book_service.create_book(title, author, publication_year, description)

        if error_message:
            errors = {'title': error_message}
            return render_template('books/form.html', form_action=url_for('book.create_book'),
                                   title=title, author=author, publication_year=publication_year,
                                   description=description, errors=errors)

        flash('Book created successfully!', 'success')
        return redirect(url_for('book.list_books'))
    return render_template('books/form.html', form_action=url_for('book.create_book'))


@book_bp.route('/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(book_id):
    book = book_service.get_book_by_id(book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.list_books'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form.get('publication_year', None)
        description = request.form['description']

        updated_book, error_message = book_service.update_book(book_id, title, author, publication_year, description)

        if error_message:
            errors = {'title': error_message}
            return render_template('books/form.html', form_action=url_for('book.update_book', book_id=book_id),
                                   book=book, errors=errors)

        flash('Book updated successfully!', 'success')
        return redirect(url_for('book.list_books'))
    return render_template('books/form.html', form_action=url_for('book.update_book', book_id=book_id), book=book)


@book_bp.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    if book_service.delete_book(book_id):
        flash('Book deleted successfully!', 'success')
    else:
        flash('Book not found!', 'danger')
    return redirect(url_for('book.list_books'))