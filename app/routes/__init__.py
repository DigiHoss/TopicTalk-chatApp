from app.routes.login import login_route
from app.routes.register import register_route
from app.routes.admin import admin_route
from app.routes.chat import chat_routes
from app.routes.logout import logout_route
from app.routes.recover_password import recover_password_routes


def init_routes(app):
    login_route(app)
    register_route(app)
    admin_route(app)
    chat_routes(app)
    logout_route(app)
    recover_password_routes(app)