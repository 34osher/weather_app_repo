import unittest
import requests


class TestWebsiteReachability(unittest.TestCase):

    def test_website_reachable(self):
        response = requests.get('http://127.0.0.1:5000')
				main
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
