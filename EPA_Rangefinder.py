import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


def create_webdriver():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.fueleconomy.gov/feg/powerSearch.jsp")
    return driver


def move_to(element, click=False, delay=0):
    action = ActionChains(driver)
    if click:
        action.move_to_element(element).click().perform()
    else:
        action.move_to_element(element).perform()
    time.sleep(delay)


def search_bev():
    set_years()
    open_vehicle_type_dropdown()
    click_all_electric()
    click_search_button()


def set_years():
    year1 = Select(driver.find_element(By.ID, "year1"))
    year1.select_by_value("2009")


def open_vehicle_type_dropdown():
    vehicle_type = driver.find_element(By.LINK_TEXT, "Vehicle Type")
    move_to(vehicle_type, click=True, delay=1)


def click_all_electric():
    all_electric_checkbox = driver.find_element(By.ID, "cbvtElectric")
    move_to(all_electric_checkbox, click=True)


def click_search_button():
    search_button = driver.find_element(By.ID, "btnSearch2")
    move_to(search_button, click=True)


driver = create_webdriver()
search_bev()

# TODO extract info from each entry based on if it is a EV
list_of_cars = driver.find_element(By.CLASS_NAME, "cars")
for car in list_of_cars.find_elements(By.CLASS_NAME, "ymm-row"):
    car_link = car.find_element(By.TAG_NAME, "a")
    car_link.click()


time.sleep(1000)
driver.close()
