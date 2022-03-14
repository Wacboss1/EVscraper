import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def create_webdriver():
    driver = webdriver.Chrome()
    driver.get("https://www.fueleconomy.gov/feg/powerSearch.jsp")
    return driver

def set_years(driver):
    year1 = Select(driver.find_element_by_id("year1"))
    year1.select_by_value("1984")


driver = create_webdriver()
set_years(driver)
driver.find_element(By.LINK_TEXT, "Vehicle Type").click()
time.sleep(3)
#TODO click checkbox for plug-in hybrids and all electrics
# just need to scroll to the element then click it (actions)
driver.find_element(By.NAME, "cbvtplugin").click()
#driver.find_element_by_id("cbvtElectric").click()
time.sleep(1000)
driver.close()