from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the database
db = SQLAlchemy()

DB_NAME = 'database.sqlite3'

def create_database(app):
    """Creates the database if it doesn't exist."""
    if not os.path.exists(f"instance/{DB_NAME}"):  # ensures proper instance folder
        with app.app_context():
            db.create_all()
            print('Database created!')

def create_app():
    """Initializes and configures the Flask app."""
    # Create Flask app instance
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ZEZO ELTANTAWE'

    # Set up the database URI (SQLite in this case)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress warnings

    # Initialize the database with the app
    db.init_app(app)

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader callback for Flask-Login
    from .models import Admin, Customer
    @login_manager.user_loader
    def load_user(user_id):
        # Try to load the user as an Admin first
        user = Admin.query.get(int(user_id))

        # If the user is not found as an Admin, try loading as a Customer
        if not user:
            user = Customer.query.get(int(user_id))

        return user


    # from .models import Customer
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return Customer.query.get(int(user_id))

    # Register blueprints
    from .auth import auth
    from .view import view
    from .admin import admin
    app.register_blueprint(auth, url_prefix='/')   # e.g., localhost:5000/auth/login
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Create the database if it doesn't exist
    with app.app_context():
        create_database(app)
    

    return app
