from flask import Flask
from app.config import init_config
from app.routes import init_routes
from app.sql_alchemy import init_db, db
from flask_login import LoginManager
from app.websocket import socketio
from app.mail_config import init_message

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    init_config(app) 
    app.secret_key = 'a7f8c2d1e49b4e6fa935b1c019da764b'
    init_routes(app)
    init_db(app)
    from app.models import User
    
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    init_message(app)
    socketio.init_app(app)


    return app