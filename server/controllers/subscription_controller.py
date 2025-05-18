from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.services.subscription_service import SubscriptionService
from server.models import db, Book, User

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')
subscription_service = SubscriptionService()


@subscription_bp.route('/')
def list_subscriptions():
    subscriptions = subscription_service.get_all_subscriptions()
    return render_template('subscription/list.html', subscriptions=subscriptions)


@subscription_bp.route('/<int:user_id>/<int:book_id>')
def view_subscription(user_id, book_id):
    subscription = subscription_service.get_subscription(user_id, book_id)

    if not subscription:
        flash('Subscription not found!', 'danger')
        return redirect(url_for('subscription.list_subscriptions'))

    user = db.session.get(User, user_id)  # Fetch user and book for display
    book = db.session.get(Book, book_id)
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
        selected_user_id = int(user_id)
        selected_book_id = int(book_id)

        success, errors = subscription_service.create_subscription(user_id, book_id)

        if errors:
            return render_template('subscription/form.html', users=users, books=books,
                                   form_action=url_for('subscription.create_subscription'),
                                   selected_user_id=selected_user_id, selected_book_id=selected_book_id,
                                   errors=errors)

        if success:
            flash('Subscription created successfully!', 'success')
            return redirect(url_for('subscription.list_subscriptions'))
        else:
            flash('Failed to create subscription!', 'danger')  # Generic error message
            return render_template('subscription/form.html', users=users, books=books,
                                   form_action=url_for('subscription.create_subscription'),
                                   selected_user_id=selected_user_id, selected_book_id=selected_book_id,
                                   errors=errors)

    return render_template('subscription/form.html', users=users, books=books,
                           form_action=url_for('subscription.create_subscription'), errors=errors)


@subscription_bp.route('/<int:user_id>/<int:book_id>/delete', methods=['POST'])
def delete_subscription(user_id, book_id):
    success, errors = subscription_service.delete_subscription(user_id, book_id)

    if errors:
        flash(errors.get('general') or 'Failed to delete subscription!', 'danger')  # Use get() for safety
    elif success:
        flash('Subscription deleted successfully!', 'success')
    else:
        flash('Failed to delete subscription!', 'danger')  # Generic error

    return redirect(url_for('subscription.list_subscriptions'))