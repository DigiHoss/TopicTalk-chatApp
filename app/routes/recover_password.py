from flask import render_template, request, redirect, url_for, flash, session
from app.models import User
from flask_mail import Message
from random import randint
from app.mail_config import mail
from app.models import db


def recover_password_routes(app):
    OTP = randint(000000, 999999) 
    
    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        email = None
        


        if request.method == "POST":
            selected_method = request.form.get("recover_method")

            if selected_method == "username":
                username = request.form.get("username")
                user = User.query.filter_by(username=username).first()
                if user:
                    email = user.email
                    session['email'] = email
                    
                    msg = Message(
                    subject="Recover your TopicTalk password",
                    sender="topictalk.contact@gmail.com",
                    recipients=[email],
                    )
                    msg.body = f"Your OTP {str(OTP)}"
                    mail.send(msg)
                    flash(f"Recovery email sent to: {email}", "success")
                    return redirect('/verify-otp')
                    
                else:
                    flash("No user found with that username.", "danger")

            elif selected_method == "email":
                email = request.form.get("email")
                session['email'] = email
                user = User.query.filter_by(email=email).first()
                if user:
                    msg = Message(
                    subject="Recover your TopicTalk password",
                    sender="topictalk.contact@gmail.com",
                    recipients=[session.get('email')],
                    )
                    msg.body = f"Your OTP {str(session.get('OTP'))}"
                    mail.send(msg)
                    flash(f"Recovery email sent to {email}", "success")
                    return redirect('/verify-otp')
                    
                else:
                    flash("No account associated with that email.", "danger")

            else:
                flash("Please select a recovery method.", "warning")

            return redirect(url_for('forgot_password'))  # On redirige pour éviter le repost

        return render_template('recoverPassword.html', email=email)
    @app.route('/verify-otp', methods=['GET', 'POST'])
    def verify():
        if request.method == 'POST':
            session_otp = session.get('OTP')
            user_otp = request.form.get('OTP')
            print(session_otp)
            print(user_otp)
            if session_otp == int(user_otp):
                flash("Please Enter your new password", 'success')
                return redirect(url_for('change_password'))  
            else:
                flash('OTP Wrong, Please try again', 'error')
            


        return redirect(url_for('forgot_password'))
    
    @app.route('/ChangePassword', methods=['GET' ,'POST'])
    def change_password():
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')
            email = session.get('email')
            if not new_password == confirm_new_password:
                flash("passwords are not the same", 'error')
            elif email:
                user = User.query.filter_by(email = email).first()
                user.set_password(new_password)

                db.session.commit()
                flash('password changed succesfully')
                return redirect(url_for('login'))
        return redirect(url_for('forgot_password'))

                


        
