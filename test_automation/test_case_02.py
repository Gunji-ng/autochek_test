# As a user, I should be able to apply filter to my search and see corresponding results.

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

PRICE_RANGE_LOWER_BOUND = 1500000
PRICE_RANGE_UPPER_BOUND = 2700000

service = Service('./chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(5)
driver.maximize_window()

def test_apply_filter_to_search():
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

    # Click the 'Price' filter item
    price_filter_item = driver.find_element_by_xpath("//span[text()='Price']/parent::div")
    price_filter_item.click()
    price_filter_modal = driver.find_element_by_xpath("//div[contains(@class, 'price-filter-container')]")
    assert price_filter_modal.is_displayed(), "Price filter modal is not displayed"

    # Set price range and click the 'Apply Filter' button
    price_range_lower_bound_input = driver.find_element_by_xpath("(//div[contains(@class, 'price-filter-container')]//input[@type='number'])[1]")
    price_range_upper_bound_input = driver.find_element_by_xpath("(//div[contains(@class, 'price-filter-container')]//input[@type='number'])[2]")
    price_range_lower_bound_input.clear()
    price_range_upper_bound_input.clear()
    apply_filter_button = driver.find_element_by_xpath("//button[contains(text(), 'Apply Filter')]")
    price_range_lower_bound_input.send_keys(PRICE_RANGE_LOWER_BOUND)
    time.sleep(5)
    price_range_upper_bound_input.send_keys(PRICE_RANGE_UPPER_BOUND)
    apply_filter_button.click()
    time.sleep(10)
    search_results = driver.find_element_by_xpath("//div[contains(@class, 'car-grid-container')]")
    filter_item_showing_price_range = driver.find_element_by_xpath("//button[contains(@class, 'filter-array-item')]")
    clear_filters_button = driver.find_element_by_xpath("//button[contains(text(), 'Clear filters')]")
    search_results_listings_prices = driver.find_elements_by_xpath("//span[@class='price']")
    assert search_results.is_displayed(), "Search results are not displayed"
    assert filter_item_showing_price_range.is_displayed()
    for listing_price in search_results_listings_prices:
        price = int((listing_price.text).replace(',' , '').strip('\u20a6 '))
        assert price >= PRICE_RANGE_LOWER_BOUND and price <= PRICE_RANGE_UPPER_BOUND
    clear_filters_button.click()
    time.sleep(5)

    service.stop()
