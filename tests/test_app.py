import unittest
import mongomock
from unittest import mock


class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.patcher = mock.patch('flask_pymongo.MongoClient', mongomock.MongoClient)
        cls.patcher.start()

        from app import app
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.patcher.stop()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register_page')
        self.assertEqual(response.status_code, 200)

    def test_register_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please fill in the below details to register.', str(response.data))

    def test_login_page(self):
        response = self.app.get('/login_page')
        self.assertEqual(response.status_code, 200)

    def test_user_reports(self):
        response = self.app.get('/user_reports')
        self.assertEqual(response.status_code, 302)

    def test_opposition_choice(self):
        response = self.app.get('/opposition_choice')
        self.assertEqual(response.status_code, 302)

    def test_create_report(self):
        response = self.app.get('/create_report/Hibs/Hearts/Tynie/Prem/261219/0-2')
        self.assertEqual(response.status_code, 302)


# Runs the tests.
if __name__ == '__main__':
    unittest.main()
