import os
import unittest



class AppTests(unittest.TestCase):

    def test_index(self):
        response = index('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()