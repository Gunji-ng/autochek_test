# As a user, I should be able to search issues and get an explanation.

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

def test_get_issue_diagnosis():
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

    # Click the 'Search issues' button
    search_issues_button.click()
    issues_wizard = driver.find_element_by_xpath("//div[@class='issue-wizard-container']")
    issues_search_box = driver.find_element_by_xpath("//input[@class='input']")
    list_of_issues = driver.find_element_by_xpath("//div[@class='issues-list']")
    assert issues_wizard.is_displayed()
    assert issues_search_box.is_displayed()
    assert list_of_issues.is_displayed()

    # Click on one of the issues in the list
    first_issue_in_list_of_issues = driver.find_element_by_xpath("//div[@class='issue-item'][1]")
    issue_text = first_issue_in_list_of_issues.text
    time.sleep(3)
    first_issue_in_list_of_issues.click()
    issue_as_a_form_header = driver.find_element_by_xpath("//div[@class='form-header']//span[@class='title']")
    issue_form_content = driver.find_element_by_xpath("//div[@class='form-content']")
    assert issue_as_a_form_header.is_displayed()
    assert issue_form_content.is_displayed()
    assert issue_text.lower() == issue_as_a_form_header.text.lower()

    # Select an answer for each question in the form-content if displayed
    time.sleep(3)

    try:
        answer_to_first_question = driver.find_element_by_xpath("((//div[@class='options'])[1]//span[@class='radio-display'])[1]")
        answer_to_first_question.click()
        time.sleep(3)
    except Exception as e:
        pass

    try:
        answer_to_second_question = driver.find_element_by_xpath("((//div[@class='options'])[2]//span[@class='radio-display'])[1]")
        answer_to_second_question.click()
        time.sleep(3)
    except Exception as e:
        pass

    try:
        answer_to_third_question = driver.find_element_by_xpath("((//div[@class='options'])[3]//span[@class='radio-display'])[1]")
        answer_to_third_question.click()
        time.sleep(3)
    except Exception as e:
        pass

    issue_explanation = driver.find_element_by_xpath("//div[@class='car-diagnosis']")
    schedule_a_call_button = driver.find_element_by_xpath("//button[contains(text(),'Schedule')]")
    assert issue_explanation.is_displayed()
    assert schedule_a_call_button.is_displayed()

    service.stop()
