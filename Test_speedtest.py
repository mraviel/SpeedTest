import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from os import path
from time import sleep

from Selenium_Classes.HomePage import HomePage


# PATH
Drivers_folder = path.join(path.dirname(__file__), 'Drivers')
chrome_driver_path = path.join(path.join(Drivers_folder, 'chromedriver'))

service_chrome = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service_chrome)

#driver.set_page_load_timeout(10)

driver.get("https://www.speedtest.net/")


driver.execute_script("window.stop();")

driver.maximize_window()
driver.implicitly_wait(10)

home_page = HomePage(driver)
home_page.click_go_button()

print(home_page.ping())

while True:
    if "opacity: 0;" in home_page.speed_handle_opacity_style():
        print(home_page.download_Mbps())
        print(home_page.upload_Mbps())
        break


driver.close()
