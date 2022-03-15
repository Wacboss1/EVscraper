import time
import re
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

# TODO extract Name,City efficiency, highway efficiency, combined efficiency, and total Range from each entry



def go_to_car_info(car):
    car_link = car.find_element(By.TAG_NAME, "a")
    move_to(car_link, click=True)


def get_car_name():
    name_element = soup.find("th", class_="sbsCellHeader")
    return " ".join(name_element.get_text().split()[1:])  # Removes "X" and whitespace


def extract_fuel_economy():
    digits = re.compile("\\d+")
    combined_fuel_economy = re.search(digits, soup.find("td", class_="combinedMPG").get_text()).group(0)
    city_fuel_economy = re.search(digits, soup.find_all("td", class_="ctyhwy")[0].get_text()).group(0)
    highway_fuel_economy = re.search(digits, soup.find_all("td", class_="ctyhwy")[1].get_text()).group(0)
    kwh_per_100miles = re.search(digits, soup.find("td", class_="fuelconsumption").get_text()).group(0)
    total_range = re.search(digits, soup.find("div", class_="totalRange").get_text()).group(0)
    return total_range, combined_fuel_economy, city_fuel_economy, highway_fuel_economy, kwh_per_100miles


list_of_cars = driver.find_element(By.CLASS_NAME, "cars")
for car in list_of_cars.find_elements(By.CLASS_NAME, "ymm-row"):
    #TODO store the href for each element then scrape each link
    go_to_car_info(car)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    name = get_car_name()
    max_range, combined, city, highway, kwh_per_100mi = extract_fuel_economy()
    driver.back()
    time.sleep(5)

time.sleep(1000)
driver.close()
