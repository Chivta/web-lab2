from server.models import db, Book

class BookDAO:
    def get_book_by_id(self, book_id):
        return db.session.get(Book, book_id)

    def get_all_books(self):
        return db.session.execute(db.select(Book)).scalars().all()

    def create_book(self, book):
        db.session.add(book)
        db.session.commit()
        return book  # Return the created book

    def update_book(self, book):
        db.session.merge(book)  # Use merge instead of add for updates
        db.session.commit()
        return book

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True  # Indicate successful deletion
        return False