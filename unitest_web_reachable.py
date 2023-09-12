import unittest
import requests


class TestWebsiteReachability(unittest.TestCase):

    def test_website_reachable(self):
        response = requests.get('http://172.31.40.84')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
