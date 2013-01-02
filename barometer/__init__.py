from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('barometer.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'


def init_db():
    db.create_all()
    from barometer.models import Amount, Category, Subcategory, User
    with app.open_resource('base_categories.txt') as f:
        Subs = []
        for line in f:
            cat, sub = line.split(',')
            if not Category.query.filter_by(category=cat).first():
                db.session.add(Category(category=cat))
                db.session.commit()
            if sub.strip():
                Subs.append(
                    Subcategory(category=cat, subcategory=sub.strip()))
        db.session.add_all(Subs)
        db.session.commit()

    with app.open_resource('base_amounts.txt') as f:
        for amount in f:
            db.session.add(Amount(amount=amount.strip()))
        db.session.commit()

    if app.debug == True:
        db.session.add(User(username='user', password='test', email='a@b.c'))
        db.session.commit()

import barometer.models
import barometer.views


@login_manager.user_loader
def load_user(userid):
    return barometer.models.User.query.get(int(userid))
