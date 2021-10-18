# As a user, I should be able to put my car up for sale.

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
USER_FULLNAME = USER_FIRSTNAME + ' ' + USER_LASTNAME
USER_EMAIL = USER_FIRSTNAME.lower() + USER_LASTNAME.lower() + '@test.com'
PHONE_NO = ''.join(random.choices(string.digits, k=10))

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
    get_started_link = driver.find_element_by_xpath("//span[text()='Get started']")
    page_title = driver.title
    assert 'Sell Cars'.lower() in page_title.lower()
    assert get_started_link.is_displayed()

    # Click the "Get started" link
    get_started_link.click()
    marketplace_wizard = driver.find_element_by_xpath("//div[@class='autochek-marketplace-container']")
    steps_breadcrumb = driver.find_element_by_xpath("//div[@class='steps']")
    assert marketplace_wizard.is_displayed()
    assert 'Car Make'.lower() in steps_breadcrumb.text.lower()

    # Select a make and click 'Next'
    first_car_make_in_list = driver.find_element_by_xpath("//div[@class='results-items']//div[@class='car-image'][1]")
    next_button = driver.find_element_by_xpath("//button[text()='Next']")
    first_car_make_in_list.click()
    next_button.click()
    assert 'Car Model'.lower() in steps_breadcrumb.text.lower()

    # Select a model and click 'Next'
    first_car_model_in_list = driver.find_element_by_xpath("//div[@class='results-items']//div[@class='car-image'][1]")
    next_button = driver.find_element_by_xpath("//button[text()='Next']")
    first_car_model_in_list.click()
    next_button.click()
    assert 'More detail'.lower() in steps_breadcrumb.text.lower()

    # Fill the other details and click Finish
    manufacture_year_field = driver.find_element_by_xpath("//label[contains(text(),'What year')]/parent::div//div[contains(@class,'input select')]")
    manufacture_year_field.click()
    driver.find_element_by_xpath("//ul[@class='select-items']//li[1]").click()
    time.sleep(3)
    body_type_field = driver.find_element_by_xpath("//label[contains(text(),'body type')]/parent::div//div[contains(@class,'input select')]")
    body_type_field.click()
    driver.find_element_by_xpath("//ul[@class='select-items']//li[1]").click()
    mileage_field = driver.find_element_by_xpath("//input[@name='mileage']")
    mileage_field.send_keys(120000)
    time.sleep(3)
    mileage_field.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    first_gear_type = driver.find_element_by_xpath("//label[contains(text(),'gear type')]/parent::div//div[@class='item'][1]")
    first_gear_type.click()
    first_fuel_type = driver.find_element_by_xpath("//label[contains(text(),'fuel type')]/parent::div//div[@class='item'][1]")
    first_fuel_type.click()
    first_condition_radio_button = driver.find_element_by_xpath("(//label[contains(@class,'radio')]//span)[1]")
    first_condition_radio_button.click()
    location_field = driver.find_element_by_xpath("//label[contains(text(),'Location')]/parent::div//div[contains(@class,'control')]/div[1]")
    location_field.click()
    first_location_option = driver.find_element_by_xpath("//div[contains(@class,'menu')]//div[contains(@id,'option-0')]")
    first_location_option.click()
    finish_button = driver.find_element_by_xpath("//button[text()='Finish']")
    time.sleep(10)
    finish_button.click()

    vehicle_details_section = driver.find_element_by_xpath("//div[@class='vehicle-details-table']")
    autochek_evaluation = driver.find_element_by_xpath("//div[@class='value']")
    continue_button = driver.find_element_by_xpath("//button[text()='Continue']")
    assert vehicle_details_section.is_displayed()
    assert autochek_evaluation.is_displayed()
    assert continue_button.is_displayed()

    # Click the Continue button
    continue_button.click()
    appointment_modal = driver.find_element_by_xpath("//div[@class='modal-form']")
    next_button = driver.find_element_by_xpath("//button[text()='Next']")
    assert appointment_modal.is_displayed()
    assert next_button.is_displayed()

    # Fill the appointment form, with the "Inspect at Autochek center" option selected. Then click "Next"
    name_field = driver.find_element_by_xpath("//input[@name='name']")
    email_address_field = driver.find_element_by_xpath("//input[@type='email']")
    phone_number_field = driver.find_element_by_xpath("//input[@type='tel']")
    inspect_at_autochek_center_option = driver.find_element_by_xpath("(//span[contains(@class,'radio-display')])[2]")
    name_field.send_keys(USER_FULLNAME)
    phone_number_field.send_keys(PHONE_NO)
    email_address_field.send_keys(USER_EMAIL)
    inspect_at_autochek_center_option.click()
    next_button.click()

    autochek_locations_modal = driver.find_element_by_xpath("//div[contains(@class,'locations-form')]")
    assert autochek_locations_modal.is_displayed()

    # Select a location
    first_location_option = driver.find_element_by_xpath("(//div[contains(@class,'select-location')])[1]")
    first_location_option.click()

    appointment_info_in_book_inspection_appointment_section = driver.find_element_by_xpath("//div[@class='selected-location']")
    submit_button = driver.find_element_by_xpath("//button[text()='Submit']")
    assert appointment_info_in_book_inspection_appointment_section.is_displayed()
    assert submit_button.is_displayed()

    # Click the Submit button
    submit_button.click()
    time.sleep(3)
    success_message = driver.find_element_by_xpath("//div[contains(text(),'Success')]")
    homepage_link = driver.find_element_by_xpath("//button[contains(text(),'Home')]")
    assert success_message.is_displayed()
    assert homepage_link.is_displayed()

    service.stop()
