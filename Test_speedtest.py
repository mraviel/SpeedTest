from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from os import path
import csv
import platform

from Selenium_Classes.HomePage import HomePage


# Which chrome driver to use
chromedriver = {'Darwin': "chromedriver_m1_mac",
                'Linux': "chromedriver_Linux64",
                'Windows': 'chromedriver_Win32.exe'}

# PATH
Drivers_folder = path.join(path.dirname(__file__), 'Drivers_v102.0.5005')
chrome_driver_path = path.join(path.join(Drivers_folder, chromedriver[platform.system()]))

service_chrome = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service_chrome)

print("Loading Page...")
driver.get("https://www.speedtest.net/")

driver.maximize_window()
driver.implicitly_wait(10)

home_page = HomePage(driver)

# Click on go
home_page.click_go_button()

ping = home_page.ping()
print(f"Ping: {ping}")

print("Computing download and upload...")
while True:
    if "opacity: 0;" in home_page.speed_handle_opacity_style():
        download_mbps = home_page.download_Mbps()
        upload_mbps = home_page.upload_Mbps()
        print(f"Download Mbps: {download_mbps} \nUpload Mbps: {upload_mbps}")
        break

# Add the values to the csv file
with open('Data/data.csv', mode='w') as data:
    writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Download', download_mbps])
    writer.writerow(['Upload', upload_mbps])
    writer.writerow(['Ping', ping])

# Close the driver
driver.close()
