# Import necessary packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# Define the name of the database file
DB_NAME = "database.db"

# Function to create and configure the Flask application
def create_app():
    # Create a Flask web application instance
    app = Flask(__name__)

    # Set a secret key for encrypting and securing cookies and data
    app.config['SECRET_KEY'] = "khdakjdfhkjdfhnkdlhfl"

    # Configure the database URI for SQLAlchemy (using SQLite in this case)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database with the Flask application
    db.init_app(app)

    # Import views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the blueprints with the Flask app and organize routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import User models
    from .models import User

    # Call the function to create the database (if it doesn't exist)
    create_database(app)

    # Setup Flask-Login for managing user sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define a function to load a user by their ID for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the configured Flask application
    return app

# Function to create the database (if it doesn't exist)
def create_database(app):
    with app.app_context():
        # Check if the database file does not exist
        if not path.exists('website/' + DB_NAME):
            # Create all the tables defined in the models
            db.create_all()
            print('Created Database!')