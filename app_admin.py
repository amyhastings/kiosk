from datetime import datetime, timedelta, timezone

from flask import Flask, flash, render_template, redirect, request, url_for, abort
from flask_login import current_user
from sqlalchemy import insert

from models import User, Role, Category, Magazine, Subscription, db

from config import app, EMPLOYEE_ROLE_ID, SUBSCRIBER_ROLE_ID, USER_ROLE_ID

@app.route('/admin/admin_console')
def admin_console():
    return render_template('admin/admin_console.html')

@app.route('/admin/add_magazine', methods=['GET', 'POST'])
def add_magazine():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        categories = Category.query.all()

        if request.method == 'POST':
            m = Magazine(title=request.form['title'], 
                        frequency=request.form['frequency'], 
                        description=request.form.get('description'), 
                        cost_per_issue=request.form.get('cost_per_issue'), 
                        cover_image=request.form.get('cover_image'),
                        employee_id=current_user.get_id())
            for category in categories:
                if "category-" + str(category.cat_id) in request.form.to_dict():
                    m.categories.append(category)
            db.session.add(m)
            db.session.commit()
            return redirect(url_for('mag_page', mag_id=m.mag_id))

        return render_template('admin/add_magazine.html', categories=categories)
    
    else:
        abort(403)

@app.route('/admin/list_magazines')
def list_magazines():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        magazines = Magazine.query.all()
        categories = Category.query.all()
        return render_template('admin/list_magazines.html', magazines=magazines, categories=categories)
    else:
        abort(403)
    
@app.route('/admin/edit_magazine/<int:mag_id>', methods=['GET', 'POST'])
def edit_magazine(mag_id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        categories = Category.query.all()
        magazine = db.get_or_404(Magazine, mag_id) 
        if request.method == 'POST':
            magazine.title = request.form['title']
            magazine.frequency = request.form['frequency']
            magazine.description = request.form['description']
            magazine.cost_per_issue = int(request.form['cost_per_issue'])
            magazine.cover_image = request.form['cover_image']
            new_categories = []
            for category in categories:
                if "category-" + str(category.cat_id) in request.form.to_dict():
                    new_categories.append(category)
            magazine.categories = new_categories

            db.session.commit()
            return redirect(url_for('mag_page', mag_id=mag_id))

        return render_template('admin/edit_magazine.html', magazine=magazine, categories=categories)
    else:
        abort(403)

@app.route('/admin/list_users')
def list_users():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        users = User.query.all()
        return render_template('admin/list_users.html', users=users)
    else:
        abort(403)

@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        roles = Role.query.all()
        user = db.get_or_404(User, id) 

        if request.method == 'POST':
            user.role_id = int(request.form['role_id'])
            user.username = request.form['username']
            user.name = request.form['name']
            user.email = request.form['email']
            user.address = request.form['address']
            db.session.commit()
            return redirect(url_for('user_page', id=id))

        return render_template('admin/edit_user.html', user=user, roles=roles)

    else:
        abort(403)

@app.route('/admin/user/<int:id>')
def user_page(id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        user = db.get_or_404(User, id) 
        print(f"Rendering the category page for {user}")
        return render_template('admin/user.html', user=user)
    else:
        abort(403)

@app.route('/admin/list_subscriptions')
def list_subscriptions():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        subscriptions = Subscription.query.all()
        users = User.query.all()
        magazines = Magazine.query.all()
        return render_template('admin/list_subscriptions.html', subscriptions=subscriptions, users=users, magazines=magazines)
    else:
        abort(403)

@app.route('/admin/edit_subscription/<int:sub_id>', methods=['GET', 'POST'])
def edit_subscription(sub_id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        subscription = db.get_or_404(Subscription, sub_id) 
        users = User.query.all()
        magazines = Magazine.query.all()

        if request.method == 'POST':
            subscription.sub_length = int(request.form['sub_length'])
            subscription.sub_start_date = datetime.strptime(request.form['sub_start_date'], '%Y-%m-%d')
            subscription.active = 'active' in request.form
            db.session.commit()
            return redirect(url_for('sub_page', sub_id=sub_id))

        return render_template('admin/edit_subscription.html', subscription=subscription, users=users, magazines=magazines)
    else:
        abort(403)

@app.route('/admin/subscription/<int:sub_id>')
def sub_page(sub_id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        subscription = db.get_or_404(Subscription, sub_id) 
        magazines = Magazine.query.all()
        users = User.query.all()
        return render_template('admin/subscription.html', subscription=subscription, users=users, magazines=magazines)
    else:
        abort(403)

@app.route('/admin/list_categories')
def list_categories():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        categories = Category.query.all()
        return render_template('admin/list_categories.html', categories=categories)
    else:
        abort(403)

@app.route('/admin/edit_category/<int:cat_id>', methods=['GET', 'POST'])
def edit_category(cat_id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        category = db.get_or_404(Category, cat_id) 
        categories = Category.query.all()

        if request.method == 'POST':
            category.cat_name = request.form['cat_name']
            db.session.commit()
            return redirect(url_for('list_categories', categories=categories))

        return render_template('admin/edit_category.html', category=category)
    else:
        abort(403)

@app.route('/admin/delete_category/<int:cat_id>', methods=['GET', 'POST'])
def delete_category(cat_id):
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        category = db.get_or_404(Category, cat_id) 
        categories = Category.query.all()
        if request.method == 'POST':
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for('list_categories', categories=categories))

        return render_template('admin/delete_category.html', category=category)
    else:
        abort(403)

@app.route('/admin/add_category', methods=['GET', 'POST'])
def add_category():
    if current_user.is_authenticated and current_user.role_id == EMPLOYEE_ROLE_ID:
        categories = Category.query.all()
        if request.method == 'POST':
            db.session.add(Category(cat_name=request.form['cat_name']))
            db.session.commit()
            return redirect(url_for('list_categories', categories=categories))

        return render_template('admin/add_category.html')
    else:
        abort(403)
