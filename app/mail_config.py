from flask_mail import Mail


mail = Mail()

def init_message(app):
    mail.init_app(app)


