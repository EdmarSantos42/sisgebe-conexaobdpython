# db_config.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# banco ficará no arquivo sgb.db na raiz do projeto
DB_PATH = os.path.join(os.path.dirname(__file__), "sgb.db")

def init_app(app: Flask) -> Flask:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app
