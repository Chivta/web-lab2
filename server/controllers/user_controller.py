from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_service = UserService()


@user_bp.route('/')
def list_users():
    users = user_service.get_all_users()
    return render_template('users/list.html', users=users)


@user_bp.route('/<int:user_id>')
def view_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('user.list_users'))
    return render_template('users/view.html', user=user)


@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        new_user, errors = user_service.create_user(username, email)

        if errors:
            return render_template('users/form.html', form_action=url_for('user.create_user'),
                                   username=username, email=email, errors=errors)

        flash('User created successfully!', 'success')
        return redirect(url_for('user.list_users'))
    return render_template('users/form.html', form_action=url_for('user.create_user'))


@user_bp.route('/<int:user_id>/update', methods=['GET', 'POST'])
def update_user(user_id):
    user = user_service.get_user_by_id(user_id)
    errors = {}
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('user.list_users'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        updated_user, errors = user_service.update_user(user_id, username, email)

        if errors:
            return render_template('users/form.html', form_action=url_for('user.update_user', user_id=user_id),
                                   user=user, errors=errors)

        flash('User updated successfully!', 'success')
        return redirect(url_for('user.list_users'))
    return render_template('users/form.html', form_action=url_for('user.update_user', user_id=user_id),
                           user=user, errors=errors)


@user_bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if user_service.delete_user(user_id):
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('user.list_users'))