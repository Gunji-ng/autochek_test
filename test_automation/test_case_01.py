# As a user, I should be able to search and get relevant results.

import pytest
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

def test_search_cars():
    # Open Autochek homepage
    driver.get('https://marketplace.staging.myautochek.com/ng')
    time.sleep(10)
    fix_your_car_link = driver.find_element_by_link_text('Fix Your Car')
    buy_a_car_link = driver.find_element_by_link_text('Buy A Car')
    sell_a_car_link = driver.find_element_by_link_text('Sell A Car')
    page_title = driver.title
    assert 'Autochek'.lower() in page_title.lower(), "'Autochek' is not in Page Title"
    assert fix_your_car_link.is_displayed(), "'Fix Your Car' link is not displayed"
    assert buy_a_car_link.is_displayed(), "'Buy A Car' link is not displayed"
    assert sell_a_car_link.is_displayed(), "'Sell A Car' link is not displayed"

    # Click the 'Buy A Car' link
    buy_a_car_link.click()
    time.sleep(10)
    cars_for_sale_header = driver.find_element_by_xpath("//h1[contains(text(), 'Cars for Sale')]")
    cars_searchbox = driver.find_element_by_xpath("//input[@class='input']")
    page_title = driver.title
    assert 'Cars for Sale'.lower() in page_title.lower(), "'Cars for Sale' is not in Page Title"
    assert cars_for_sale_header.is_displayed(), "'Cars for Sale' header is not displayed"
    assert cars_searchbox.is_displayed(), "Search box for cars is not displayed"

    # Type SEARCH_DATA into the searchbox and press Enter
    cars_searchbox.send_keys(SEARCH_DATA)
    cars_searchbox.send_keys(Keys.ENTER)
    time.sleep(10)
    search_results = driver.find_element_by_xpath("//div[contains(@class, 'car-grid-container')]")
    search_results_listings_names = driver.find_elements_by_xpath("//span[@class='name']")
    search_results_listings_years = driver.find_elements_by_xpath("//span[@class='year']")
    assert search_results.is_displayed(), "Search results are not displayed"
    for listing_name in search_results_listings_names:
        assert listing_name.text == CAR_MODEL
    for listing_year in search_results_listings_years:
        assert listing_year.text == MANUFACTURE_YEAR

    service.stop()
