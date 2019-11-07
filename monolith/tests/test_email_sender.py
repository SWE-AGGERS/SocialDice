import unittest
from monolith.database import db, User, Followers, Story
from monolith.tests.restart_db import restart_db_tables
from monolith.app import create_app
from monolith.background import *
from monolith.views.follow import _create_follow

_app = None
 
# THIS WILL FAIL IF YOU DON'T ADD USER+PASSWORD in COSTANTS.py
class TestEmailSender(unittest.TestCase):
    def test_email_sender(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                example2 = User()
                example2.firstname = 'Daniele'
                example2.lastname = 'Arioli'
                example2.email = 'intotheroom101@gmail.com'
                example2.dateofbirth = datetime(2020, 10, 5)
                example2.is_admin = True
                example2.set_password('admin')
                db.session.add(example2)
                db.session.commit()

                self.assertTrue(send_emails())

