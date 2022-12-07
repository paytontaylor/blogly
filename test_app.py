from app import app
from unittest import TestCase
from models import db

class UserViewsTestCase(TestCase):

    def setUp(self):
        return 

    def tearDown(self):
        db.session.rollback() 

    def test_show_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_add_user_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)

    

    

