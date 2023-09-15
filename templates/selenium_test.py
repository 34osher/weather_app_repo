import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLocationResponse(unittest.TestCase):

    def setUp(self):
        # Initialized the Selenium WebDriver (IDE)
        self.driver = webdriver.Firefox()

    def test_positive_location_response(self):
        # Open the web page
        self.driver.get('http://localhost:5000')

        # Enter a valid location in the input field and submit the form
        location_input = self.driver.find_element(By.ID, 'location')
        location_input.send_keys('New York')
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        # Check if the weather data table is displayed
        weather_table = self.driver.find_element(By.CSS_SELECTOR, 'table')
        self.assertTrue(weather_table.is_displayed())

    def test_negative_location_response(self):
        # Open the web page
        self.driver.get('http://localhost:5000')

        # Enter an invalid location in the input field and submit the form
        location_input = self.driver.find_element(By.ID, 'location')
        location_input.send_keys('InvalidLocation123')
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        # Check if an error message is displayed
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p.error')
        self.assertTrue(error_message.is_displayed())

    def tearDown(self):
        # Close the WebDriver after each test
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
