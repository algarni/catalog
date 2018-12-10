from app import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)


db.event.listen(User.__table__, 'after_create',
                db.DDL("""
                    INSERT INTO user (id, email) 
                    VALUES (1, 'm.t.algarni@gmail.com')
                """))

db.event.listen(Category.__table__, 'after_create',
                db.DDL("""
                    INSERT INTO category (id, name) 
                    VALUES (1, 'Computers'), 
                    (2, 'Computer peripherals'), 
                    (3, 'Data storage'),
                    (4, 'Printers'),
                    (5, 'Data center devices'),
                    (6, 'Desktop devices'),
                    (7, 'Network components'), 
                    (8, 'Software')
                """))



db.event.listen(Item.__table__, 'after_create',
                db.DDL("""
                    INSERT INTO item (id, name, description, category_id, user_id) 
                    VALUES (1, 'Mainframe', 'Mainframe computers are computers used primarily by large organizations for critical applications; bulk data processing, such as census, industry and consumer statistics, enterprise resource planning; and transaction processing.', 1, 1), 
                    (2, 'Servers', 'A server is a computer that serves data or prov"id"es access to an application (such as a database, e-mail) to more than one person.', 1, 1), 
                    (3, 'Desktop computer', 'Desktop computers are typically dedicated to only one person at a desk or work station.', 1, 1),
                    (4, 'Laptop', 'i.  A laptop is a computer, screen, storage and keyboard all in one unit. It can be removed from the workstation and carried around.', 1, 1),
                    (5, 'Tablet and other mobile devices', 'A tablet is a computer with the screen, processor and storage in a single unit. A smartphones are classified as cellular phones.', 1, 1)
                """))