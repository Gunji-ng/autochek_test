# As a user, I should be able to schedule a pre-sale vehicle inspection successfully.

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import random
import string

RANDOM_STRING = ''.join(random.choices(string.ascii_lowercase, k=4))
USER_FIRSTNAME = 'Test' + RANDOM_STRING
USER_LASTNAME = 'User' + RANDOM_STRING
USER_EMAIL = USER_FIRSTNAME.lower() + USER_LASTNAME.lower() + '@test.com'
PHONE_NO = ''.join(random.choices(string.digits, k=10))
CAR_MODEL = 'Toyota Camry 2010'

service = Service('./chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(5)
driver.maximize_window()

def test_schedule_presale_vehicle_inspection():
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

    # Click the 'Sell A Car' link
    sell_a_car_link.click()
    time.sleep(10)
    pre_sale_vehicle_inspection_form = driver.find_element_by_xpath("//div[@class='inspection-form']")
    page_title = driver.title
    assert "Sell Cars".lower() in page_title.lower()
    assert pre_sale_vehicle_inspection_form.is_displayed()

    # Fill the inspection form and submit
    first_name_field = driver.find_element_by_xpath("//input[@name='firstName']")
    last_name_field = driver.find_element_by_xpath("//input[@name='lastName']")
    email_address_field = driver.find_element_by_xpath("//input[@type='email']")
    phone_number_field = driver.find_element_by_xpath("//input[@type='tel']")
    car_model_field = driver.find_element_by_xpath("//input[@name='car']")
    submit_button = driver.find_element_by_xpath("//button[text()='Submit']")

    first_name_field.send_keys(USER_FIRSTNAME)
    last_name_field.send_keys(USER_LASTNAME)
    phone_number_field.send_keys(PHONE_NO)
    email_address_field.send_keys(USER_EMAIL)
    car_model_field.send_keys(CAR_MODEL)
    time.sleep(3)
    submit_button.click()

    time.sleep(3)
    success_message = driver.find_element_by_xpath("//div[contains(text(),'Success')]")
    homepage_link = driver.find_element_by_xpath("//button[contains(text(),'Home')]")
    assert success_message.is_displayed()
    assert homepage_link.is_displayed()

    service.stop()
