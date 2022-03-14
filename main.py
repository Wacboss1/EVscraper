import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Open Webdriver
driver = webdriver.Chrome()
driver.get("https://www.fueleconomy.gov/feg/powerSearch.jsp")


driver.close()