import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def create_webdriver():
    driver = webdriver.Chrome()
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


def extract_all_car_links():
    car_link_list = []
    while True:
        current_page = extract_current_page_num()
        add_car_links_to_list(car_link_list)
        click_next_page()
        new_page = extract_current_page_num()
        if is_still_same_page(current_page, new_page):
            break
    return car_link_list


def add_car_links_to_list(car_link_list):
    soup = update_soup()
    cars = soup.find_all("tr", class_="ymm-row")
    for car in cars:
        car_link_list.append(car.find("a").get("href"))


def update_soup():
    return BeautifulSoup(driver.page_source, 'lxml')


def click_next_page():
    next_button = driver.find_element(By.CLASS_NAME, "icon-next")
    move_to(next_button, click=True)


def extract_current_page_num():
    soup = update_soup()
    new_page = soup.find("ul", class_="pagination").get_text().strip()
    return new_page


def is_still_same_page(current_page, new_page):
    return current_page == new_page


def extract_ev_data():
    global soup
    driver.get("https://www.fueleconomy.gov/feg/" + link)
    soup = update_soup()
    name = get_car_name()
    return name, extract_fuel_economy()


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
    return total_range, city_fuel_economy, highway_fuel_economy, combined_fuel_economy, kwh_per_100miles


def create_datasheet():
    global link
    electric_vehicles = pd.DataFrame()
    for link in car_link_list:
        model, fuel_econ = extract_ev_data()
        entry = {"Model": model, "Range": fuel_econ[0],
                 "City Efficiency": fuel_econ[1], "Highway Efficiency": fuel_econ[2],
                 "Combined Efficiency": fuel_econ[3],
                 "Kwh/100mi": fuel_econ[4]}
        electric_vehicles = electric_vehicles.append(entry, ignore_index=True)
    electric_vehicles.to_csv("US EV Fuel Economy Dataset.csv")


driver = create_webdriver()
search_bev()
soup = update_soup()
car_link_list = extract_all_car_links()
create_datasheet()
driver.close()
