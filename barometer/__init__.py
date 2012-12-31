from __future__ import with_statement

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
# FIXME: Move to config file
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/barometer.db'
SQLALCHEMY_ECHO = True
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


def init_db():
    db.create_all()
    from barometer.models import Category, Subcategory, Amount
    with app.open_resource('base_categories.txt') as f:
        Subs = []
        for line in f:
            cat, sub = line.split(',')
            if not Category.query.filter_by(category=cat).first():
                db.session.add(Category(category=cat))
                db.session.commit()
            Subs.append(
                Subcategory(category=cat, subcategory=sub.strip()))
        db.session.add_all(Subs)
        db.session.commit()

    with app.open_resource('base_amounts.txt') as f:
        for amount in f:
            db.session.add(Amount(amount=amount.strip()))
        db.session.commit()

import barometer.models
import barometer.views
