import unittest
from app import create_app, db
from app.models.User import User
from app.models.Role import Role


class BaseTestCase(unittest.TestCase):
    """Base Tests"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        db.session.commit()

        Role.insert_roles()
        User.insert_root_admin()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
