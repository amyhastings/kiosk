from datetime import datetime, timedelta, timezone

from flask import Flask, flash, render_template, redirect, request, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import insert

from models import User, Magazine, Subscription, Role, db

from config import app, EMPLOYEE_ROLE_ID, SUBSCRIBER_ROLE_ID, USER_ROLE_ID

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        if User.query.filter_by(username=username).first():
            flash(f"The username '{username}' is already taken")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash(f"The email '{email}' is already taken")
            return redirect(url_for("register"))

        user = User(username=username, name=name, email=email, password=password, address=address)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome {username}!")
        return redirect(url_for("home"))
    
    return render_template("users/register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(f"No such user '{username}'")
            return redirect(url_for("login"))
        if password != user.password:
            flash(f"Invalid password for the user '{username}'")
            return redirect(url_for("login"))

        login_user(user)
        flash(f"Welcome back, {username}!")
        return redirect(url_for("home"))

    return render_template("users/login.html")

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash("You have been logged out")
        return redirect(url_for("home"))

    return render_template("users/logout.html")

@app.route('/my_account')
def my_account():
    if current_user.is_authenticated:
        return render_template('users/my_account.html')
    else:
        return redirect(url_for("login"))

@app.route('/my_account/my_details')
def my_details():
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.id)
        return render_template('users/my_details.html', user=user)
    else:
        return redirect(url_for("login"))
    
@app.route('/my_account/edit_my_details', methods=['GET', 'POST'])
def edit_my_details():
    if current_user.is_authenticated:
        user = User.query.filter_by(user_id=current_user.id)

        if request.method == 'POST':
            user.username = request.form['username']
            user.name = request.form['name']
            user.email = request.form['email']
            user.address = request.form['address']
            db.session.commit()
            return redirect(url_for('my_details'))

        return render_template('users/edit_my_details.html', user=user)

    else:
        return redirect(url_for("login"))

@app.route('/my_account/my_subscriptions')
def my_subscriptions():
    if current_user.is_authenticated:
        subscriptions = Subscription.query.filter_by(user_id=current_user.id)
        return render_template('users/my_subscriptions.html', subscriptions=subscriptions)
    else:
        return redirect(url_for("login"))

@app.route('/subscribe/<int:mag_id>', methods=['GET', 'POST'])
def add_subscription(mag_id):
    magazine = db.get_or_404(Magazine, mag_id) 
    if request.method == 'POST':
        s = Subscription(
            user_id = current_user.get_id(),
            mag_id=request.form['mag_id'], 
            sub_length=request.form['sub_length'],
            sub_start_date=datetime.now(),
            active=True
            )
        db.session.add(s)
        if current_user.role_id == USER_ROLE_ID:
            current_user.role_id = SUBSCRIBER_ROLE_ID
        db.session.commit()
        return redirect(url_for('my_subscriptions', sub_id=s.sub_id, magazine=magazine))

    return render_template('users/subscribe.html', magazine=magazine)