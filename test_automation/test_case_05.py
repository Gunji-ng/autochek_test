# As a user, I should be able to schedule a car service appointment successfully.

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

def test_book_car_service_appointment():
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

    # Click the 'Fix Your Car' link
    fix_your_car_link.click()
    time.sleep(10)
    chat_with_autodoctor_button = driver.find_element_by_xpath("//a[contains(@href,'whatsapp') or text()='Chat with me']")
    search_issues_button = driver.find_element_by_xpath("//button[text()='Search issues']")
    list_of_services = driver.find_element_by_xpath("//div[@class='services-list']")
    page_title = driver.title
    assert "Car Repair & Maintenance".lower() in page_title.lower()
    assert chat_with_autodoctor_button.is_displayed()
    assert search_issues_button.is_displayed()
    assert list_of_services.is_displayed()

    # Click on one of the listed Services
    first_listed_service = driver.find_element_by_xpath("//div[@class='service-item'][1]")
    name_of_first_listed_service = first_listed_service.text
    first_listed_service.click()
    time.sleep(10)
    service_name_as_a_header = driver.find_element_by_xpath("//h1")
    service_details = driver.find_element_by_xpath("//div[@class='service-details-content']")
    appointment_form = driver.find_element_by_xpath("//div[@class='inspection-form']")
    assert name_of_first_listed_service.lower() == service_name_as_a_header.text.lower()
    assert service_details.is_displayed()
    assert appointment_form.is_displayed()

    # Fill the appointment form and click "Confirm appointment"
    full_name_field = driver.find_element_by_xpath("//input[@name='name']")
    email_address_field = driver.find_element_by_xpath("//input[@type='email']")
    phone_number_field = driver.find_element_by_xpath("//input[@type='tel']")
    car_model_field = driver.find_element_by_xpath("//div[contains(@class,'control')]")
    drop_off_at_autochek_location_option = driver.find_element_by_xpath("//label[contains(text(),'Autochek location')]")
    confirm_appointment_button = driver.find_element_by_xpath("//button[text()='Confirm appointment']")
    full_name_field.send_keys(USER_FULLNAME)
    phone_number_field.send_keys(PHONE_NO)
    email_address_field.send_keys(USER_EMAIL)
    car_model_field.click()
    first_car_model_in_dropdown = driver.find_element_by_xpath("//div[contains(@class,'menu')]//div[contains(@id,'option-0')]")
    first_car_model_in_dropdown.click()
    drop_off_at_autochek_location_option.click()
    first_autochek_service_center_option = driver.find_element_by_xpath("(//div[contains(text(), 'Select location')])[1]")
    first_autochek_service_center_option.click()
    confirm_appointment_button.click()

    appointment_booked_message = driver.find_element_by_xpath("//div[contains(text(),'appointment has been booked')]")
    homepage_link = driver.find_element_by_xpath("//button[contains(text(),'Home')]")
    assert appointment_booked_message.is_displayed()
    assert homepage_link.is_displayed()

    service.stop()
