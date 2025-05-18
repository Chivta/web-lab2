from server.dao.subscription_dao import SubscriptionDAO
from server.models import db, User, Book

class SubscriptionService:
    def __init__(self):
        self.subscription_dao = SubscriptionDAO()

    def get_all_subscriptions(self):
        return self.subscription_dao.get_all_subscriptions()

    def get_subscription(self, user_id, book_id):
        return self.subscription_dao.get_subscription(user_id, book_id)

    def create_subscription(self, user_id, book_id):
        user = db.session.get(User, user_id)
        book = db.session.get(Book, book_id)

        errors = {}
        if not user:
            errors['user_id'] = 'User not found!'
        if not book:
            errors['book_id'] = 'Book not found!'
        if self.get_subscription(user_id, book_id):
            errors['general'] = 'Subscription already exists!'

        if errors:
            return False, errors  # Return False to indicate failure and errors

        self.subscription_dao.create_subscription(user_id, book_id)
        return True, None  # Return True to indicate success and no errors

    def delete_subscription(self, user_id, book_id):
        user = db.session.get(User, user_id)
        book = db.session.get(Book, book_id)

        errors = {}
        if not user:
            errors['user_id'] = 'User not found!'
        if not book:
            errors['book_id'] = 'Book not found!'
        if not self.get_subscription(user_id, book_id):
            errors['general'] = 'Subscription not found!'

        if errors:
            return False, errors  # Return False to indicate failure and errors

        self.subscription_dao.delete_subscription(user_id, book_id)
        return True, None  # Return True to indicate success and no errors