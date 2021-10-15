import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

CAR_MODEL = 'Toyota Camry'
MANUFACTURE_YEAR = '2010'
SEARCH_DATA = CAR_MODEL + ' ' + MANUFACTURE_YEAR

service = Service('./chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(5)
driver.maximize_window()
driver.get('https://marketplace.staging.myautochek.com/ng')
buy_a_car_link = driver.find_element_by_link_text('Buy A Car')
buy_a_car_link.click()
search_results_listings_prices = driver.find_elements_by_xpath("//span[@class='price']")
print(search_results_listings_prices)
for i in search_results_listings_prices:
    b = i.text
    print(int(b.replace("," , "").strip("\u20a6 ")))
