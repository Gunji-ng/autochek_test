# As a user, I should be able to create an account and sign in with created account.

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
USER_EMAIL = USER_FIRSTNAME.lower() + USER_LASTNAME.lower() + '@email.com'
USER_PASSWORD = USER_LASTNAME.lower()
PHONE_NO = ''.join(random.choices(string.digits, k=10))

service = Service('./chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(5)
driver.maximize_window()

def test_register_and_login():
    # Open Autochek homepage
    driver.get('https://marketplace.staging.myautochek.com/ng')
    time.sleep(10)
    sign_in_link = driver.find_element_by_link_text('Sign In')
    register_link = driver.find_element_by_link_text('Register')
    page_title = driver.title
    assert 'Autochek'.lower() in page_title.lower(), "'Autochek' is not in Page Title"
    assert sign_in_link.is_displayed(), "'Sign In' link is not displayed"
    assert register_link.is_displayed(), "'Register' link is not displayed"

    # Click the Register link
    register_link.click()
    time.sleep(10)
    registration_form = driver.find_element_by_xpath("//form[@class='form-content']")
    create_account_button = driver.find_element_by_xpath("//button[@type='submit']")
    page_title = driver.title
    assert 'Register'.lower() in page_title.lower()
    assert registration_form.is_displayed()
    assert create_account_button.is_displayed()

    # Fill the registration form and click Create Account
    first_name_field = driver.find_element_by_xpath("//input[@type='firstname']")
    last_name_field = driver.find_element_by_xpath("//input[@type='lastname']")
    email_address_field = driver.find_element_by_xpath("//input[@type='email']")
    phone_number_field = driver.find_element_by_xpath("//input[@type='tel']")
    password_field = driver.find_element_by_xpath("//input[@type='password']")
    first_name_field.send_keys(USER_FIRSTNAME)
    last_name_field.send_keys(USER_LASTNAME)
    email_address_field.send_keys(USER_EMAIL)
    phone_number_field.send_keys(PHONE_NO)
    time.sleep(2)
    password_field.clear()
    password_field.send_keys(USER_PASSWORD)
    time.sleep(2)
    create_account_button.click()
    time.sleep(20)
    logged_in_user_profile_icon = driver.find_element_by_xpath("//div[@class='profile-menu']//a[1]")
    sign_out_link = driver.find_element_by_link_text('Sign Out')
    assert logged_in_user_profile_icon.is_displayed()
    assert sign_out_link.is_displayed()

    # Click the sign out link
    sign_out_link.click()
    time.sleep(10)

    sign_in_link = driver.find_element_by_link_text('Sign In')
    assert sign_in_link.is_displayed()

    # Click the sign in link
    sign_in_link.click()
    time.sleep(10)
    login_email_address_field = driver.find_element_by_xpath("//input[@type='email']")
    login_password_field = driver.find_element_by_xpath("//input[@type='password']")
    login_button = driver.find_element_by_xpath("//button[@type='submit']")
    page_title = driver.title
    assert 'Login'.lower() in page_title.lower()
    assert login_email_address_field.is_displayed()
    assert login_password_field.is_displayed()
    assert login_button.is_displayed()

    # Fill the email address and password fields and click Log In
    login_email_address_field.send_keys(USER_EMAIL)
    time.sleep(2)
    login_password_field.clear()
    login_password_field.send_keys(USER_PASSWORD)
    time.sleep(2)
    login_button.click()
    time.sleep(10)
    logged_in_user_profile_icon = driver.find_element_by_xpath("//div[@class='profile-menu']//a[1]")
    sign_out_link = driver.find_element_by_link_text('Sign Out')
    assert logged_in_user_profile_icon.is_displayed()
    assert sign_out_link.is_displayed()

    service.stop()
