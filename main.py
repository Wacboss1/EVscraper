import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def create_webdriver():
    driver = webdriver.Chrome()
    driver.get("https://www.fueleconomy.gov/feg/powerSearch.jsp")
    return driver

def set_years(driver):
    year1 = Select(driver.find_element_by_id("year1"))
    year1.select_by_value("1984")

# Open Webdriver
driver = create_webdriver()
set_years(driver)
time.sleep(1000)
driver.close()