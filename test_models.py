from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """ Test Model for User """

    def setUp(self):
        """ Clean up any existing pets in the test db """

        User.query.delete()

    def tearDown(self):
        """ Clean up any unwanted transactions """

        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name='FirstName', last_name='LastName')
        self.assertEquals(user.get_full_name(), 'FirsName LastName')