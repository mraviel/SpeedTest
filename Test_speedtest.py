from unittest import TestCase
import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from os import path
import csv
import platform

from Selenium_Classes.HomePage import HomePage


class TestSpeedtest(TestCase):
    """ Test speedtest site """

    def setUp(self):

        # Which chrome driver to use
        chromedriver = {'Darwin': "chromedriver_m1_mac",
                        'Linux': "chromedriver_Linux64",
                        'Windows': 'chromedriver_Win32.exe'}

        # PATH
        Drivers_folder = path.join(path.dirname(__file__), 'Drivers_v102.0.5005')
        chrome_driver_path = path.join(path.join(Drivers_folder, chromedriver[platform.system()]))

        service_chrome = Service(chrome_driver_path)

        self.driver = webdriver.Chrome(service=service_chrome)
        self.driver.set_page_load_timeout(15)  # Set max time for page to load

        # Load the page until timeout than start testing
        print("Loading Page...")
        try:
            self.driver.get("https://www.speedtest.net/")
        except TimeoutException:
            pass

        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.home_page = HomePage(self.driver)

    def test_1(self):
        """ Test that ping, download and upload have value
            And print them into csv file: Data/data.csv """

        self.home_page.click_go_button()
        ping = self.home_page.ping()
        print(f"Ping: {ping}")

        print("Computing download and upload...")
        while True:
            if "opacity: 0;" in self.home_page.speed_handle_opacity_style():
                download_mbps = self.home_page.download_Mbps()
                upload_mbps = self.home_page.upload_Mbps()
                print(f"Download Mbps: {download_mbps} \nUpload Mbps: {upload_mbps}")
                break

        # Verify the data have content (Not None or Empty)
        for data in [ping, download_mbps, upload_mbps]:
            self.assertTrue(data)

        # add the values to the csv file
        with open('Data/data.csv', mode='w') as data:
            writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Download', download_mbps])
            writer.writerow(['Upload', upload_mbps])
            writer.writerow(['Ping', ping])

    def tearDown(self):

        # Close the driver
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
