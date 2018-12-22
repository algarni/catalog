#!/usr/bin/env python3

from app import db
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(256))
    username = db.Column(db.String(256), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'id': self.id,
        }


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(265), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Item {}>'.format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


# db.event.listen(User.__table__, 'after_create',
#                 db.DDL("""
#                     INSERT INTO "user" (id, email, name, username) 
#                     VALUES (1, 'm.t.algarni@gmail.com', 'Mohammad Algarni', 'admin')
#                 """))

def insert_user_initial_values(*args, **kwargs):
    db.session.add(User(email='m.t.algarni@gmail.com', name='Mohammad Algarni', username='admin'))
    db.session.commit()

db.event.listen(User.__table__, 'after_create', insert_user_initial_values)

# db.event.listen(Category.__table__, 'after_create',
#                 db.DDL("""
#                     INSERT INTO category (id, name) 
#                     VALUES (1, 'Computers'), 
#                     (2, 'Computer peripherals'), 
#                     (3, 'Data storage'),
#                     (4, 'Printers'),
#                     (5, 'Data center devices'),
#                     (6, 'Desktop devices'),
#                     (7, 'Network components'), 
#                     (8, 'Software')
#                 """))

def insert_category_initial_values(*args, **kwargs):
    user = db.session.query(User).filter_by(email='m.t.algarni@gmail.com').one()
    db.session.add(Category(name='Computer'))
    db.session.commit()

db.event.listen(Category.__table__, 'after_create', insert_category_initial_values)


# db.event.listen(Item.__table__, 'after_create',
#                 db.DDL("""
#                     INSERT INTO item (id, name, description, category_id, user_id) 
#                     VALUES (1, 'Mainframe', 'Mainframe computers are computers used primarily by large organizations for critical applications; bulk data processing, such as census, industry and consumer statistics, enterprise resource planning; and transaction processing.', 1, 1), 
#                     (2, 'Servers', 'A server is a computer that serves data or prov"id"es access to an application (such as a database, e-mail) to more than one person.', 1, 1), 
#                     (3, 'Desktop computer', 'Desktop computers are typically dedicated to only one person at a desk or work station.', 1, 1),
#                     (4, 'Laptop', 'i.  A laptop is a computer, screen, storage and keyboard all in one unit. It can be removed from the workstation and carried around.', 1, 1),
#                     (5, 'Tablet and other mobile devices', 'A tablet is a computer with the screen, processor and storage in a single unit. A smartphones are classified as cellular phones.', 1, 1)
#                 """))

def insert_item_initial_values(*args, **kwargs):
    user = db.session.query(User).filter_by(email='m.t.algarni@gmail.com').one()
    category = db.session.query(Category).filter_by(name='Computer').one()
    db.session.add(Item(name='Mainframe', description='Mainframe computers are computers used primarily by large organizations for critical applications; bulk data processing, such as census, industry and consumer statistics, enterprise resource planning; and transaction processing.', category_id=category.id, user_id=user.id))
    db.session.commit()

db.event.listen(Item.__table__, 'after_create', insert_item_initial_values)