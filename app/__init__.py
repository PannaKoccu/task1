# Flask modules
from flask import Flask
import os
from dotenv import load_dotenv  # <-- новый импорт

def create_app(debug: bool = False) -> Flask:
    # Загружаем переменные из .env (если файл существует)
    load_dotenv()

    # Initialize app
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')

    # Setup app configs
    app.config['DEBUG'] = debug
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-insecure-key-for-development-only')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///database.db'  # fallback — только для локальной разработки
    )

    # Initialize extensions
    from app.extensions import db, bcrypt, csrf, login_manager
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Create database tables
    from app import models
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
