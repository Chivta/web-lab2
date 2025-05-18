from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.models import db, Book, User, user_book_subscription

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')


@subscription_bp.route('/')
def list_subscriptions():
    subscriptions = db.session.query(
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
    return render_template('subscription/list.html', subscriptions=subscriptions)

#
@subscription_bp.route('/<int:user_id>/<int:book_id>')
def view_subscription(user_id, book_id):
    user = db.session.get(User, user_id)
    book = db.session.get(Book, book_id)

    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))  # Redirect to subscription list

    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))  # Redirect to subscription list

    subscription_exists = db.session.query(user_book_subscription).filter_by(user_id=user_id, book_id=book_id).first()

    if not subscription_exists:
        flash('Subscription not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))

    return render_template('subscription/view.html', user=user, book=book)


def get_subscription_form_data():
    """Helper function to get data for the subscription form."""
    users = db.session.execute(db.select(User)).scalars().all()
    books = db.session.execute(db.select(Book)).scalars().all()
    return users, books


@subscription_bp.route('/create', methods=['GET', 'POST'])
def create_subscription():
    users, books = get_subscription_form_data()
    errors = {}
    selected_user_id = None
    selected_book_id = None

    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        selected_user_id = int(user_id)  # Ensure integer for comparison
        selected_book_id = int(book_id)

        user = db.session.get(User, user_id)
        book = db.session.get(Book, book_id)

        if not user:
            errors['user_id'] = 'User not found!'
        if not book:
            errors['book_id'] = 'Book not found!'
        subscription_exists = db.session.query(user_book_subscription).filter_by(user_id=user_id, book_id=book_id).first()
        if subscription_exists:
            errors['general'] = 'Subscription already exists!'

        if errors:
            return render_template('subscription/form.html', users=users, books=books,
                                   form_action=url_for('subscription.create_subscription'),
                                   selected_user_id=selected_user_id, selected_book_id=selected_book_id, errors=errors)

        new_subscription = user_book_subscription.insert().values(user_id=user_id, book_id=book_id,
                                                                  date_added=datetime.now())
        db.session.execute(new_subscription)
        db.session.commit()

        flash('Subscription created successfully!', 'success')
        return redirect(url_for('subscription.list_subscriptions'))

    # Якщо GET запит, відображаємо форму для створення підписки
    return render_template('subscription/form.html', users=users, books=books,
                           form_action=url_for('subscription.create_subscription'), errors=errors)


# @subscription_bp.route('/<int:user_id>/<int:book_id>/update', methods=['GET', 'POST'])
# def update_subscription(user_id, book_id):
#     user = db.session.get(User, user_id)
#     book = db.session.get(Book, book_id)
#     if request.method == 'POST':
#         if not user:
#             flash('User not found!', 'danger')
#             return redirect(url_for('subscription.list_subscriptions'))
#
#         if not book:
#             flash('Book not found!', 'danger')
#             return redirect(url_for('subscription.list_subscriptions'))
#
#         # Перевіряємо, чи існує підписка
#         subscription = db.session.query(user_book_subscription).filter_by(user_id=user_id, book_id=book_id).first()
#         if not subscription:
#             flash('Subscription not found!', 'danger')
#             return redirect(url_for('subscription.list_subscriptions'))
#
#         # if request.method == 'POST':
#         # Отримуємо дані з форми (наприклад, нова дата)
#         # new_date = request.form['new_date']
#
#         # Оновлюємо дані підписки (якщо є що оновлювати)
#         # subscription.date = new_date
#         db.session.commit()
#         flash('Subscription updated successfully!', 'success')
#         return redirect(url_for('subscription.view_subscription', user_id=user_id, book_id=book_id))
#
#     # Якщо GET запит, відображаємо форму для оновлення
#     return render_template('subscription/form.html', user=user, book=book,
#                            form_action=url_for('subscription.update_subscription', user_id=user_id, book_id=book_id))


@subscription_bp.route('/<int:user_id>/<int:book_id>/delete', methods=['POST'])
def delete_subscription(user_id, book_id):
    """Видалення підписки користувача на книгу."""
    user = db.session.get(User, user_id)
    book = db.session.get(Book, book_id)

    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))

    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))

    # Перевіряємо, чи існує підписка
    subscription = db.session.query(user_book_subscription).filter_by(user_id=user_id, book_id=book_id).first()
    if not subscription:
        flash('Subscription not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))

    # Видаляємо підписку
    delete_stmt = user_book_subscription.delete().where(user_book_subscription.c.user_id == user_id).where(
        user_book_subscription.c.book_id == book_id)
    db.session.execute(delete_stmt)
    db.session.commit()

    flash('Subscription deleted successfully!', 'success')
    return redirect(url_for('subscription.list_subscriptions'))