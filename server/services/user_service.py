from server.dao.user_dao import UserDAO
from server.models import User

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def get_user_by_id(self, user_id):
        return self.user_dao.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_dao.get_all_users()

    def create_user(self, username, email):
        # Validation logic here (e.g., check if user exists)
        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        errors = {}
        if existing_user_username:
            errors['username'] = 'Username already exists'
        if existing_user_email:
            errors['email'] = 'Email already exists'

        if errors:
            return None, errors

        new_user = User(username=username, email=email)
        return self.user_dao.create_user(new_user), None

    def update_user(self, user_id, username, email):
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            return None, "User not found!"

        existing_user_username = User.query.filter_by(username=username).filter(User.id != user_id).first()
        existing_user_email = User.query.filter_by(email=email).filter(User.id != user_id).first()

        errors = {}
        if existing_user_username:
            errors['username'] = 'Username already exists'
        if existing_user_email:
            errors['email'] = 'Email already exists'

        if errors:
            return None, errors

        user.username = username
        user.email = email
        return self.user_dao.update_user(user), None

    def delete_user(self, user_id):
        return self.user_dao.delete_user(user_id)