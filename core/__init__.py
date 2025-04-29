from flask import Flask
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'quiz.db'  # путь к файлу базы данных

    # Регистрируй blueprint'ы и другие настройки
    from .routes import bp
    app.register_blueprint(bp)

    # Вызов инициализации базы данных, чтобы создать таблицы
    init_db(app)

    return app
