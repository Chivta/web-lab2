from server.models import db, User, Book, user_book_subscription
from datetime import datetime

class SubscriptionDAO:
    def get_all_subscriptions(self):
        return db.session.query(
            User.username,
            Book.title,
            db.func.strftime('%Y-%m-%d %H:%M', user_book_subscription.c.date_added).label('date_added'),
            User.id.label('User_id'),
            Book.id.label('Book_id')
        ).join(
            user_book_subscription, User.id == user_book_subscription.c.user_id
        ).join(
            Book, Book.id == user_book_subscription.c.book_id
        ).all()

    def get_subscription(self, user_id, book_id):
        return db.session.query(user_book_subscription).filter_by(user_id=user_id, book_id=book_id).first()

    def create_subscription(self, user_id, book_id):
        new_subscription = user_book_subscription.insert().values(
            user_id=user_id, book_id=book_id, date_added=datetime.now()
        )
        db.session.execute(new_subscription)
        db.session.commit()

    def delete_subscription(self, user_id, book_id):
        delete_stmt = user_book_subscription.delete().where(
            user_book_subscription.c.user_id == user_id
        ).where(
            user_book_subscription.c.book_id == book_id
        )
        db.session.execute(delete_stmt)
        db.session.commit()