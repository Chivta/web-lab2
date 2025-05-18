from server.dao.book_dao import BookDAO
from server.models import Book

class BookService:
    def __init__(self):
        self.book_dao = BookDAO()

    def get_book_by_id(self, book_id):
        return self.book_dao.get_book_by_id(book_id)

    def get_all_books(self):
        return self.book_dao.get_all_books()

    def create_book(self, title, author, publication_year, description):
        # Validation logic here (e.g., check if book exists)
        existing_book = Book.query.filter_by(title=title, author=author).first()
        if existing_book:
            return None, "A book with this title and author already exists!"  # Return None and error message

        new_book = Book(title=title, author=author, publication_year=publication_year, description=description)
        return self.book_dao.create_book(new_book), None

    def update_book(self, book_id, title, author, publication_year, description):
        book = self.book_dao.get_book_by_id(book_id)
        if not book:
            return None, "Book not found!"

        existing_book = Book.query.filter_by(title=title, author=author).filter(Book.id != book_id).first()
        if existing_book:
            return None, "A book with this title and author already exists!"

        book.title = title
        book.author = author
        book.publication_year = publication_year
        book.description = description
        return self.book_dao.update_book(book), None

    def delete_book(self, book_id):
        return self.book_dao.delete_book(book_id)