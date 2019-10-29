import os
import sqlalchemy
import unittest
from monolith import app
from monolith.database import User
from werkzeug.security import generate_password_hash
import json

class LoginTestCase(unittest.TestCase):

    def testLoginPage(self):
        response = self.getTester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)



    def setUp(self):
        user1 = User()
        user1.firstname = "selman"
        user1.lastname = "alpdundar"
        user1.email = "selman.alp@hotmail.com.tr"
        user1.dateofbirth = "1994"
        user1.password = user1.set_password("12345")

        user2 = User()
        user2.firstname = "ahmet"
        user2.lastname = "kaya"
        user2.email = "kaya@gmail.com"
        user2.dateofbirth = "1978"
        user2.password = user2.set_password("67891")

    @property
    def getTester(self):
        applitation = app.create_app()
        tester = applitation.test_client(self)
        return tester


if __name__ == '__main__':
    unittest.main()
