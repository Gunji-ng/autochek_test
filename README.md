# autochek_test

This repo contains automated tests for Autochek's staging website.
Each test is written using Selenium webdriver for python and the entire suite is to be run using Pytest.

I chose Selenium because it is straightforward and can be used to mimic user interactions.
Getting information about the page's current state is also hassle-free.
Using Selenium tests the web app from the user's perspective which is the most important.

I chose Pytest to run the test suite as it is more concise and has less boilerplate code.
It can also be extended with several plugins.
