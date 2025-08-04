from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()
Base = db.Model

# database initialization
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return db