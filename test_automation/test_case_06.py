# As a user, I should be able to chat with Autochek Autodoctor.

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

def test_chat_with_autodoctor():
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

    # Click the "Chat with me" button
    initial_tab = driver.window_handles[0]
    chat_with_autodoctor_button.click()
    time.sleep(10)
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)
    autochek_header = driver.find_element_by_xpath("//h1[contains(text(),'Autochek')]")
    message_textbox = driver.find_element_by_xpath("//div[@id='main_block']/div[2]/div")
    default_message = message_textbox.text
    continue_to_chat_button = driver.find_element_by_xpath("//a[@id='action-button']")
    page_title = driver.title
    assert "Share on WhatsApp".lower() in page_title.lower()
    assert autochek_header.is_displayed()
    assert "Hi AutoDoctor".lower() in default_message.lower()
    assert continue_to_chat_button.is_displayed()

    service.stop()
