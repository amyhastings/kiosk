from datetime import date

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config import USER_ROLE_ID

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.mapped_column(db.Integer, primary_key=True)
    role_id = db.mapped_column(db.Integer, db.ForeignKey('roles.role_id'), default=USER_ROLE_ID)
    username = db.mapped_column(db.String(50), unique=True)
    name = db.mapped_column(db.String(100))
    email = db.mapped_column(db.String(200), unique=True)
    password = db.mapped_column(db.String(80))
    address = db.mapped_column(db.String(200))

    roles = relationship('Role', back_populates='users', uselist=False)
    subscriptions = relationship('Subscription', back_populates='users', uselist=True) 
    magazines = relationship('Magazine', back_populates='users', uselist=True) 

    def __repr__(self):
        return f'User<username={self.username}, role_id={self.role_id}>'

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(20))

    users = relationship('User', back_populates='roles')

    def __repr__(self):
        return f'Role<title={self.title}, role_id={self.role_id}>'

mag_to_categories = Table('mag_to_categories', db.metadata,
    Column('cat_id', Integer, ForeignKey('categories.cat_id')),
    Column('mag_id', Integer, ForeignKey('magazines.mag_id'))
)

class Category(db.Model):
    __tablename__ = 'categories'
    cat_id = db.mapped_column(db.Integer, primary_key=True)
    cat_name = db.mapped_column(db.String(50))

    magazines = relationship('Magazine', secondary=mag_to_categories, back_populates='categories')

    def __repr__(self):
        return f'{self.cat_name}'

class Magazine(db.Model):
    __tablename__ = 'magazines'
    mag_id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(100))
    frequency = db.mapped_column(db.String(20), nullable=False)
    description = db.mapped_column(db.String(1500))
    cost_per_issue = db.mapped_column(db.Integer, nullable=False) #this will need to be in cents
    cover_image = db.mapped_column(db.String(100))
    employee_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    subscriptions = relationship('Subscription', back_populates='magazines', uselist=True) #this is one (mag) to many (subs)
    categories = relationship('Category', secondary=mag_to_categories, back_populates='magazines')
    users = db.relationship('User', back_populates='magazines') #this is one to one

    def __repr__(self):
        return f'Magazine<title={self.title}, mag_id={self.mag_id}>'

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    sub_id = db.mapped_column(db.Integer, primary_key=True)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mag_id = db.mapped_column(db.Integer, db.ForeignKey('magazines.mag_id'), nullable=False)
    sub_length = db.mapped_column(db.Integer) #number of issues
    sub_start_date = db.mapped_column(db.Date)
    active = db.mapped_column(db.Boolean, nullable=False)

    users = db.relationship('User', back_populates='subscriptions') #this is one to one
    magazines = db.relationship('Magazine', back_populates='subscriptions') # there is only one (mag) for each sub (one) - this is caught under one-to-many mag to sub relationship

    def __repr__(self):
        return f'Subscription<sub_id={self.sub_id}, mag_id={self.mag_id}, active={self.active}>'
    
    def get_next_month(self, d):
        if d.month == 12:
            return date(d.year + 1, 1, 1)
        else:
            return date(d.year, d.month + 1, 1)
        
    def get_next_quarter(self, d):
        if d.month == 1 or d.month == 2 or d.month == 3:
            return date(d.year, 4, 1)
        elif d.month == 4 or d.month == 5 or d.month == 6:
            return date(d.year, 7, 1)
        elif d.month == 7 or d.month == 8 or d.month == 9:
            return date(d.year, 10, 1)
        elif d.month == 10 or d.month == 11 or d.month == 12:
            return date(d.year + 1, 1, 1)
        else:
            raise Exception('Invalid date exception.')

    def get_first_issue_date(self):
        start_dt = self.sub_start_date
        if self.magazines.frequency == 'Monthly':
            return (self.get_next_month(self.sub_start_date))
        elif self.magazines.frequency == 'Quarterly':
            return (self.get_next_quarter(self.sub_start_date))
        else:
            raise Exception('Magazine has invalid frequency.')

