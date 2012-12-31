from flask import render_template

from barometer import app
from barometer.models import Amount, Bottle, Category, Subcategory


@app.route("/")
@app.route("/<category>")
def index(category=None):
    if category:
        results = Bottle.query.filter_by(category=category).all()
        if not results:
            results = Bottle.query.filter_by(subcategory=category).all()
    else:
        results = Bottle.query.all()
    return render_template('index.html', bottles=results, category=category)


@app.route("/add")
def add():
    return render_template('unimplemented.html', page='Add')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
