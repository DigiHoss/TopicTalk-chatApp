from flask import render_template
from app.models import User


def admin_route(app):
    @app.route('/dashboard')
    def admin():
        return render_template('dashboard.html', users=User.query.all())
