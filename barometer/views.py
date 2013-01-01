from flask import flash, render_template, request

from barometer import app, db
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


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        form = request.form
        NewBottle = Bottle(
            form['description'],
            form['category'].lower(),
            form['subcategory'].lower(),
            form['size'],
            form['amount'].lower())
        db.session.add(NewBottle)
        db.session.commit()
        flash('%s was added to your inventory' % NewBottle)
    lists = dict(
        categories=Category.query.all(),
        subcategories=Subcategory.query.all(),
        amounts=Amount.query.all())
    return render_template('add_bottle.html', **lists)


@app.route("/delete")
def delete():
    return render_template('unimplemented.html', page='Delete')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
