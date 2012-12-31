from flask import abort, render_template

from barometer import app
from barometer.models import Amount, Bottle, Category, Subcategory


@app.route("/")
def index(category=None):
    if category:
        results = Bottle.query.filter_by(category=category).all()
        if not results:
            results = Bottle.query.filter_by(category=category).all()
        if not results:
            abort(404)
    else:
        results = Bottle.query.all()
    return render_template('index.html', bottles=results)
