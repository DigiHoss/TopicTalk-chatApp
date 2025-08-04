from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, current_user
import re


def login_route(app):

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username_email = request.form.get('identifier')

            password = request.form.get('password')
            from app.models import User
            if is_email(username_email):
                user = User.query.filter_by(email = username_email).first()
            else :
                user = User.query.filter_by(username = username_email).first()


            #user = authenticate_user(username, password)

            if user and user.check_password(password):
                # session['username'] = username
                login_user(user)
                return redirect(url_for('room'))

            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')
    
        return render_template('login.html')
    
def is_email(input_str):

    return re.match(r"[^@]+@[^@]+\.[^@]+", input_str)

