import os

from flask import Flask, render_template

from server.models import db

def create_app():
    app = Flask(__name__,template_folder='client/templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # Use SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.urandom(24)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')


    # Import and register blueprints (controllers) here
    from server.controllers import book_controller, user_controller, subscription_controller
    app.register_blueprint(book_controller.book_bp)
    app.register_blueprint(user_controller.user_bp)
    app.register_blueprint(subscription_controller.subscription_bp)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)  # Run the app in debug mode