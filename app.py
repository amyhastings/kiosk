from datetime import datetime, timedelta, timezone

from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import insert

from models import User, Role, Category, Magazine, Subscription, mag_to_categories, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

with app.app_context():
    db.init_app(app)
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html', categories=Category.query.all())

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

@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin')
def admin_console():
    return render_template('admin.html')

@app.route('/add_magazine', methods=['GET', 'POST'])
def add_magazine():
    categories = Category.query.all()
    # u = User.query.get(int(2))
    # # u = User.query.get(int(user_id))

    if request.method == 'POST':
        m = Magazine(title=request.form['title'], 
                     frequency=request.form['frequency'], 
                     description=request.form.get('description'), 
                     cost_per_issue=request.form.get('cost_per_issue'), 
                     cover_image=request.form.get('cover_image'),
                     employee_id=2)
        for category in categories:
            if "category-" + str(category.cat_id) in request.form.to_dict():
                m.categories.append(category)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('mag_page', mag_id=m.mag_id))

    categories = Category.query.all()
    return render_template('add_magazine.html', categories=categories)

@app.route('/list_magazines')
def list_magazines():
    magazines = Magazine.query.all()
    categories = Category.query.all()
    return render_template('list_magazines.html', magazines=magazines, categories=categories)


@app.route('/edit_magazine/<int:mag_id>', methods=['GET', 'POST'])
def edit_magazine(mag_id):
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

    return render_template('edit_magazine.html', magazine=magazine, categories=categories)


@app.route('/list_users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    print(request.form.to_dict())
    roles = Role.query.all()
    user = db.get_or_404(User, user_id) 
    # u = User.query.get(int(2))
    # # u = User.query.get(int(user_id))

    if request.method == 'POST':
        user.role_id = int(request.form['role_id'])
        user.username = request.form['username']
        user.name = request.form['name']
        user.email = request.form['email']
        user.address = request.form['address']
        db.session.commit()
        return redirect(url_for('user_page', user_id=user_id))

    return render_template('edit_user.html', user=user, roles=roles)

@app.route('/user/<int:user_id>')
def user_page(user_id):
    user = db.get_or_404(User, user_id) 
    print(f"Rendering the category page for {user}")
    return render_template('user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user_filter(user_id):
    user = db.get_or_404(User, user_id) 
    if int(user.role_id) == 3:
        return render_template('delete_user.html', user=user)
    
    return render_template('cannot_delete_user.html', user=user)

@app.route('/delete_user_query/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id) 
    users = User.query.all()
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('list_users', users=users))

    return render_template('delete_user.html', user=user)

@app.route('/list_subscriptions')
def list_subscriptions():
    subscriptions = Subscription.query.all()
    users = User.query.all()
    magazines = Magazine.query.all()
    return render_template('list_subscriptions.html', subscriptions=subscriptions, users=users, magazines=magazines)

@app.route('/edit_subscription/<int:sub_id>', methods=['GET', 'POST'])
def edit_subscription(sub_id):
    subscription = db.get_or_404(Subscription, sub_id) 
    users = User.query.all()
    magazines = Magazine.query.all()

    if request.method == 'POST':
        subscription.sub_length = int(request.form['sub_length'])
        subscription.sub_start_date = datetime.strptime(request.form['sub_start_date'], '%Y-%m-%d')
        subscription.active = 'active' in request.form
        db.session.commit()
        return redirect(url_for('sub_page', sub_id=sub_id))

    return render_template('edit_subscription.html', subscription=subscription, users=users, magazines=magazines)

@app.route('/subscription/<int:sub_id>')
def sub_page(sub_id):
    subscription = db.get_or_404(Subscription, sub_id) 
    magazines = Magazine.query.all()
    users = User.query.all()
    return render_template('subscription.html', subscription=subscription, users=users, magazines=magazines)

if __name__ == '__main__':
    app.run(debug=True, port=8080)