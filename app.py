from datetime import datetime, timedelta, timezone

from flask import Flask, flash, render_template, redirect, request, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import insert

from models import User, Role, Category, Magazine, Subscription, mag_to_categories, db

from config import app, EMPLOYEE_ROLE_ID, SUBSCRIBER_ROLE_ID, USER_ROLE_ID

from app_admin import admin_console, add_magazine, list_magazines, edit_magazine, list_users, \
    edit_user, user_page, list_subscriptions, edit_subscription, sub_page, list_categories, \
        edit_category, delete_category, add_category

from app_users import register, login, logout, my_account, my_details, edit_my_details, my_subscriptions, add_subscription

app.config.from_object('config')  # Load configuration from config.py

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

with app.app_context():
    db.init_app(app)
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.context_processor
def inject_employee_role_id():
    return dict(EMPLOYEE_ROLE_ID=EMPLOYEE_ROLE_ID)

@app.context_processor
def inject_subscriber_role_id():
    return dict(SUBSCRIBER_ROLE_ID=SUBSCRIBER_ROLE_ID)

@app.route('/')
def home():
    return render_template('home.html', magazines = Magazine.query.all())

@app.route('/all_categories')
def all_categories():
    return render_template('all_categories.html', categories=Category.query.all())

@app.route('/category/<int:cat_id>')
def category_mags(cat_id):
    category = db.get_or_404(Category, cat_id) 
    print(f"Rendering the category page for {category}")
    return render_template('category.html', category=category)

@app.route('/magazine/<int:mag_id>')
def mag_page(mag_id):
    magazine = db.get_or_404(Magazine, mag_id) 
    print(f"Rendering the category page for {magazine}")
    return render_template('magazine.html', magazine=magazine)

if __name__ == '__main__':
    app.run(debug=True, port=8080)