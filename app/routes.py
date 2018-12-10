from flask import render_template, request, redirect, url_for, flash
from app import app, db
from .models import Category, Item, User


# categories = [{"name": 'Computers', "id": 1},
#               {"name": 'Computer peripherals', "id": 2},
#               {"name": 'Data storage', "id": 3},
#               {"name": 'Printers', "id": 4},
#               {"name": 'Data center devices', "id": 5},
#               {"name": 'Desktop devices', "id": 6},
#               {"name": 'Network components', "id": 7},
#               {"name": 'Software', "id": 8}
#               ]


# items = [
#     {"id": 1, "name": 'Mainframe', "description": 'Mainframe computers are computers used primarily by large organizations for critical applications; bulk data processing, such as census, industry and consumer statistics, enterprise resource planning; and transaction processing.', 'category_name': 'Computers'},
#     {"id": 2, "name": 'Servers',
#         "description": 'A server is a computer that serves data or prov"id"es access to an application (such as a database, e-mail) to more than one person.', 'category_name': 'Computers'},
#     {"id": 3, "name": 'Desktop computer',
#         "description": 'Desktop computers are typically dedicated to only one person at a desk or work station.', 'category_name': 'Computers'},
#     {"id": 4, "name": 'Laptop', "description": 'i.  A laptop is a computer, screen, storage and keyboard all in one unit. It can be removed from the workstation and carried around.', 'category_name': 'Computers'},
#     {"id": 5, "name": 'Tablet and other mobile devices',
#         "description": 'A tablet is a computer with the screen, processor and storage in a single unit. A smartphones are classified as cellular phones.', 'category_name': 'Computers'}
# ]


@app.before_first_request
def create_database():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@app.route('/login')
def login():
    pass


@app.route('/logout')
def logout():
    pass


@app.route('/catalog/categories')
def showCategoreis():
    return render_template('categories.html')


@app.route('/catalog/category/new')
def newCategory():
    return render_template('newCategory.html')


@app.route('/catalog/<category_name>/edit')
def editCategory(category_name):
    return render_template('editCategory.html', category=category)


@app.route('/catalog/<category_name>/delete')
def deleteCategory(category_name):
    return render_template('deleteCategory.html', category=category)


@app.route('/catalog/<category_name>/items')
def showItems(category_name):
    category = Category.query.filter_by(name=category_name).first()
    items = Item.query.filter_by(category_id=category.id)
    return render_template('items.html', category=category, items=items)


@app.route('/catalog/<category_name>/item/new', methods=['GET', 'POST'])
def newItem(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if request.method == 'POST':
        itemName = request.form['itemName']
        description = request.form['description']
        item = Item(name=itemName, description=description,
                    category_id=category.id)
        db.session.add(item)
        db.session.commit()
        flash('New item has been created')
        return redirect(url_for('showItems', category_name=category.name))
    else:
        return render_template('newItem.html', category=category)


@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(name=item_name).first()
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


@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    category = Category.query.filter_by(name=category_name).first()
    item = Item.query.filter_by(name=item_name).first()
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('"{}" has been deleted'.format(item.name))
        return redirect(url_for('showItems', category_name=category.name))
    else:
        return render_template('deleteItem.html', category=category, item=item)
