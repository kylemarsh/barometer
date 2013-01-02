from flask.ext.login import UserMixin

from barometer import db


class Bottle(db.Model):
    __tablename__ = 'bottles'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(
            db.String(15),
            db.ForeignKey('categories.category'))
    subcategory = db.Column(
            db.String(15),
            db.ForeignKey('subcategories.subcategory'))
    description = db.Column(db.Text)
    size = db.Column(db.String(15))
    amount = db.Column(db.String(15), db.ForeignKey('amounts.amount'))

    def __init__(
            self,
            description,
            category,
            subcategory,
            size,
            amount):

        self.description = description
        self.category = category
        self.subcategory = subcategory
        self.size = size
        self.amount = amount

    def __repr__(self):
        return "<Bottle(%s, %s, %s, %s, %s)>" % (
            self.description,
            self.category,
            self.subcategory,
            self.size,
            self.amount)

    def __str__(self):
        if self.amount == 'full' or self.amount == 'mostly full':
            quantity = "A %s %s bottle" % (self.amount, self.size)
        else:
            quantity = "%s of a %s bottle" % (self.amount, self.size)

        if self.subcategory:
            kind = "%s %s" % (self.subcategory, self.category)
        else:
            kind = self.category

        return "%s of %s %s" % (quantity, self.description, kind)


class Category(db.Model):
    __tablename__ = 'categories'

    category = db.Column(db.String(15), primary_key=True)

    def __str__(self):
        return self.category


class Subcategory(db.Model):
    __tablename__ = 'subcategories'

    category = db.Column(
        db.String(15),
        db.ForeignKey('categories.category'),
        primary_key=True)
    subcategory = db.Column(db.String(15), primary_key=True)


class Amount(db.Model):
    __tablename__ = 'amounts'

    amount = db.Column(db.String(15), primary_key=True)

    def __str__(self):
        return self.amount


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(63))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
