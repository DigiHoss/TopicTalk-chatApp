from flask import render_template, request, redirect, url_for, flash



def register_route(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            from app.models import User
            from app.sql_alchemy import db
            
            username = request.form.get('username')
            password = request.form.get('password')
            confirm = request.form.get('confirm_password')
            email = request.form.get('email')
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            
            if existing_user or existing_email:
                if existing_user:
                    flash("Username already exists!", "error")
                if existing_email:
                    flash("Email already exists!", "error")
                return render_template("register.html")
            
            if not password == confirm:
                flash("Two passwords are not the same")

            else:
                try:
                    # Create new user
                    new_user = User(username=username, email=email)
                    new_user.set_password(password)
                    
                    db.session.add(new_user)
                    db.session.commit()
                    
                    flash('Thanks for registering! You can now log in.', 'success')
                    return redirect(url_for('login'))
                    
                except Exception as e:
                    db.session.rollback()
                    flash('An error occurred during registration. Please try again.', 'error')
                    return render_template("register.html")
            
        return render_template("register.html")