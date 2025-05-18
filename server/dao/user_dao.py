from server.models import db, User

class UserDAO:
    def get_user_by_id(self, user_id):
        return db.session.get(User, user_id)

    def get_all_users(self):
        return db.session.execute(db.select(User)).scalars().all()

    def create_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        db.session.merge(user)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False