# As a user, I should be able to see the necessary information when I click on a listing.

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

service = Service('./chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(5)
driver.maximize_window()

def test_view_listing_details():
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
    search_results = driver.find_element_by_xpath("//div[contains(@class, 'car-grid-container')]")
    assert 'Cars for Sale'.lower() in page_title.lower(), "'Cars for Sale' is not in Page Title"
    assert cars_for_sale_header.is_displayed(), "'Cars for Sale' header is not displayed"
    assert cars_searchbox.is_displayed(), "Search box for cars is not displayed"
    assert search_results.is_displayed(), "Search results are not displayed"

    # Click on a listing from the results
    first_listing_in_results = driver.find_element_by_xpath("(//div[@class='car-item'])[1]//a")
    listing_name = driver.find_element_by_xpath("(//div[@class='car-item'])[1]//span[@class='name']")
    listing_year = driver.find_element_by_xpath("(//div[@class='car-item'])[1]//span[@class='year']")
    name_of_listing = listing_name.text
    year_of_listing = listing_year.text
    listing_brief = name_of_listing + ' ' + year_of_listing
    first_listing_in_results.click()
    time.sleep(10)
    page_title = driver.title
    car_summary_section = driver.find_element_by_xpath("//div[contains(@class,'car-summary-container')]")
    vehicle_description_section = driver.find_element_by_xpath("//div[contains(@class,'vehicle-description-container')]")
    key_features_section = driver.find_element_by_xpath("//div[contains(@class,'key-features-container')]")
    assert listing_brief.lower() in page_title.lower(), "Car model and year not in Page Title"
    assert car_summary_section.is_displayed(), "Car summary section not displayed"
    assert vehicle_description_section.is_displayed(), "Vehicle description section not displayed"
    assert key_features_section.is_displayed(), "Key features section not displayed"


    service.stop()
