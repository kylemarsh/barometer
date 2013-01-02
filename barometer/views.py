from flask import flash, render_template, redirect, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from barometer import app, db
from barometer.models import Amount, Bottle, Category, Subcategory, User


@app.route("/")
@app.route("/<search>")
def index(search=None):
    if search:
        try:
            subcat, cat = search.split()
            results = Bottle.query.filter_by(category=cat, subcategory=subcat).all()
        except ValueError:
            results = None
        if not results:
            results = Bottle.query.filter_by(category=search).all()
        if not results:
            results = Bottle.query.filter_by(subcategory=search).all()
    else:
        results = Bottle.query.all()

    categories = {bottle.category: [] for bottle in results}
    for bottle in results:
        categories[bottle.category].append(bottle)

    return render_template('index.html', categories=categories, search=search)


@app.route("/add", methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        form = request.form
        category = form['category']
        subcategory = form['subcategory']
        try:
            if form['category'] == 'new':
                category = add_category(form['new_category'])
            if form['subcategory'] == 'new':
                subcategory = add_subcategory(
                    category,
                    form['new_subcategory'])
            NewBottle = Bottle(
                form['description'],
                category,
                subcategory,
                form['size'],
                form['amount'].lower())
            db.session.add(NewBottle)
            db.session.commit()
            flash('%s was added to your inventory' % NewBottle)
        except CategoryError:
            flash('%s is not a valid category' % category)

    lists = dict(
        categories=Category.query.all(),
        subcategories=Subcategory.query.all(),
        amounts=Amount.query.all())
    return render_template('add_bottle.html', **lists)


@app.route("/delete")
@app.route("/delete/<bottle_id>")
@login_required
def delete(bottle_id=None):
    if bottle_id:
        bottle = Bottle.query.get_or_404(bottle_id)
        db.session.delete(bottle)
        db.session.commit()
        flash('%s was removed from your inventory' % bottle)

    results = Bottle.query.all()

    categories = {bottle.category: [] for bottle in results}
    for bottle in results:
        categories[bottle.category].append(bottle)

    return render_template('delete_bottle.html', categories=categories)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = auth_user(username, password)
        if user:
            remember = request.form.get("remember", "no") == "1"
            login_user(user, remember=remember)
            flash("Welcome, %s" % user.username)
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Bad username or password")
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def add_category(new_category):
    new_category = new_category.strip().lower()
    if Category.query.filter_by(category=new_category).first():
        app.logger.debug('category %s already exists' % new_category)
        return new_category
    db.session.add(Category(category=new_category))
    db.session.commit()
    return new_category


def add_subcategory(category, new_subcategory):
    new_subcategory = new_subcategory.strip().lower()
    if not Category.query.filter_by(category=category).first():
        # we don't have the category...abort
        app.logger.error('category %s does not exist; ' % category +
            'cannot create subcategory')
        raise CategoryError
    if Subcategory.query.filter_by(subcategory=new_subcategory).first():
        app.logger.debug('subcategory %s.%s already exists' %
        (category, new_subcategory))
        return new_subcategory
    db.session.add(Subcategory(
        category=category,
        subcategory=new_subcategory))
    db.session.commit()
    return new_subcategory


def auth_user(username, password):
    #FIXME: password currently stored in cleartext
    return User.query.filter_by(username=username, password=password).first()


class CategoryError(Exception):
    """Raised when something tries to use a nonexistant category
    """
