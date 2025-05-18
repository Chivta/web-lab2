from flask import Blueprint, render_template, redirect, url_for, request, flash
from server.models import db, User

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('users/list.html', users=users)


@user_bp.route('/<int:user_id>')
def view_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('user.list_users'))
    return render_template('users/view.html', user=user)


@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # Перевірка на існування користувача з таким username або email
        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        errors = {}
        if existing_user_username:
            errors['username'] = 'Username already exists'
        if existing_user_email:
            errors['email'] = 'Email already exists'

        if errors:
            return render_template('users/form.html', form_action=url_for('user.create_user'), username=username,
                                   email=email, errors=errors)

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('user.list_users'))
    return render_template('users/form.html', form_action=url_for('user.create_user'))


@user_bp.route('/<int:user_id>/update', methods=['GET', 'POST'])
def update_user(user_id):
    user = db.session.get(User, user_id)
    errors = {}
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('user.list_users'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

    # Перевірка на існування користувача з таким username або email (крім поточного)
        existing_user_username = User.query.filter_by(username=username).filter(User.id != user_id).first()
        existing_user_email = User.query.filter_by(email=email).filter(User.id != user_id).first()

        if existing_user_username:
            errors['username'] = 'Username already exists'
        if existing_user_email:
            errors['email'] = 'Email already exists'

        if errors:
            return render_template('users/form.html', form_action=url_for('user.update_user', user_id=user_id), user=user,
                                   errors=errors)

        user.username = username
        user.email = email
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('user.list_users'))
    return render_template('users/form.html', form_action=url_for('user.update_user', user_id=user_id), user=user, errors=errors)

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    return redirect(url_for('user.list_users'))