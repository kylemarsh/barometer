import os
import barometer
import unittest
import tempfile


class BarometerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_fn = tempfile.mkstemp()
        barometer.app.config['SQLALCHEMY_ECHO'] = False
        barometer.app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///%s" % self.db_fn
        barometer.app.config['TESTING'] = True
        self.app = barometer.app.test_client()
        barometer.init_db()

    def tearDown(self):
        barometer.db.drop_all()
        #os.close(self.db_fd)
        #os.unlink(self.db_fn)

    def test_init_db(self):
        from barometer.models import Amount, Category, Subcategory
        amounts = Amount.query.all()
        self.assertEqual([a.amount for a in amounts],
            ['full', 'most', '3/4', 'half', '1/3', '1/4', 'dregs'])

        categories = Category.query.all()
        self.assertEqual([c.category for c in categories],
            ['vodka', 'tequila', 'gin', 'rum', 'whiskey', 'vermouth',
            'cognac', 'brandy', 'liqueur', 'flavor', 'cooking'])

        subcategories = Subcategory.query.all()
        self.assertEqual(len(subcategories), 27)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'hooligans' in rv.data

    def test_bottle_string(self):
        from barometer.models import Bottle
        bottle = Bottle('description', 'type', 'subtype', 'size', 'amount')
        self.assertEqual(
            '%s' % bottle,
            'amount of a size bottle of description subtype type')

if __name__ == "__main__":
    unittest.main()
