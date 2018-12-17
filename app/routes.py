#!/usr/bin/env python3

from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db, login, blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.google import google
from sqlalchemy.orm.exc import NoResultFound
from .models import Category, Item, User, OAuth
from flask_login import current_user, login_user, login_required, logout_user


@app.before_first_request
def create_database():
    db.create_all()


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# setup SQLAlchemy backend for OAuth
blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@login.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('google.login'))


# on successful OAuth login, existing user can login. New users will
# registered first in database before login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash('Log in failed with Google.', categroy='error')
        return False

    response = blueprint.session.get('/oauth2/v2/userinfo')

    if not response.ok:
        message = 'Fetching user informaton has been failed from Google.'
        flash(message, category='error')
        return False

    authenticated_user_info = response.json()
    authenticated_user_id = str(authenticated_user_info['id'])

    # search for this OAuth token in the database, or create a new one
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=authenticated_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=authenticated_user_id,
            token=token,
        )
    if oauth.user:
        login_user(oauth.user)
        flash('You have signed in seccessfully with Google.')

    else:
        # Check if the user exist in the database
        try:
            user = User.query.filter_by(
                email=authenticated_user_info['email']).one()
        except NoResultFound:
            # Create a new local user account for this authenticated user
            user = User(
                email=authenticated_user_info['email'],
                name=authenticated_user_info['name'],
                username=authenticated_user_info['email']
            )

        # Update OAuth token with local user information
        oauth.user = user
        db.session.add(user)
        db.session.add(oauth)
        db.session.commit()

        # Log in the new user using his local account
        login_user(user)
        flash('You have successfully signed in with Google.')

    return False


@app.route('/')
@app.route('/index')
def index():
    # categories = Category.query.all()
    # return render_template('categories.html', categories=categories)
    return redirect(url_for('showCategories'))


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('google.login'))
    token = blueprint.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": "ya29.Glx0BkOLfor79Qg6kmNTIUs3Hnv61Zs6bA6xaW17jJmZiui3tm5QybewYpGRAUp3EBkePWI7OMeHJCTXjde1egQiwzvGBN8DVUZC7wGnWklk2zLPcDFMmVUFZTA7fA"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    logout_user()
    flash('You have successfully logged out of your account')
    return redirect(url_for('index'))


@app.route('/catalog/categories')
def showCategories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@app.route('/catalog/categories/JSON')
def showCategoriesJSON():
    categories = Category.query.all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/catalog/category/new')
def newCategory():
    # TODO
    return render_template('newCategory.html')


@app.route('/catalog/<category_name>/edit')
def editCategory(category_name):
    # TODO
    return render_template('editCategory.html', category=category)


@app.route('/catalog/<category_name>/delete')
def deleteCategory(category_name):
    # TODO
    return render_template('deleteCategory.html', category=category)


@app.route('/catalog/<category_name>/items')
def showItems(category_name):
    category = Category.query.filter_by(name=category_name).first()
    items = Item.query.filter_by(category_id=category.id)
    return render_template('items.html', category=category, items=items)


@app.route('/catalog/<category_name>/items/JSON')
def showItemsJSON(category_name):
    category = Category.query.filter_by(name=category_name).first()
    items = Item.query.filter_by(category_id=category.id)
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<category_name>/item/new', methods=['GET', 'POST'])
@login_required
def newItem(category_name):

    category = Category.query.filter_by(name=category_name).first()
    if request.method == 'POST':
        itemName = request.form['itemName']
        description = request.form['description']
        item = Item(name=itemName, description=description,
                    category_id=category.id, user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        flash('New item has been created')
        return redirect(url_for('showItems', category_name=category.name))
    else:
        return render_template('newItem.html', category=category)


@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_name):

    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(name=item_name).first()

    # If item does not belong to the authenticated user, the user will not be
    # authorised to edit the item
    if item.user_id != current_user.id:
        return render_template('403.html'), 403

    if request.method == 'POST':
        item.name = request.form['itemName']
        item.description = request.form['description']
        db.session.commit()
        flash('Item has been edited')
        return redirect(url_for('editItem', category_name=category.name, item_name=item.name))
    else:
        return render_template('editItem.html', category=category, item=item)


@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(
        name=item_name, category_id=category.id).first()
    return render_template('itemDetail.html', category=category, item=item)


@app.route('/catalog/<category_name>/<item_name>/JSON')
def showItemJSON(category_name, item_name):
    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(
        name=item_name, category_id=category.id).first()
    return jsonify(
        id=item.id,
        name=item.name,
        description=item.description,
    )


@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_name):

    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(name=item_name).first()

    # If item does not belong to the authenticated user, the user will not be
    # authorised to edit the item
    if item.user_id != current_user.id:
        return render_template('403.html'), 403

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('"{}" has been deleted'.format(item.name))
        return redirect(url_for('showItems', category_name=category.name))
    else:
        return render_template('deleteItem.html', category=category, item=item)
