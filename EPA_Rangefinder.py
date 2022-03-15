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
    global soup, name
    driver.get("https://www.fueleconomy.gov/feg/" + link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    name = get_car_name()
    return name, extract_fuel_economy()


print("creating driver")
driver = create_webdriver()
print("searching for cars")
search_bev()
print("gathering links")
soup = update_soup()
car_link_list = extract_all_car_links()
print("extracting data")
for link in car_link_list:
    ev = extract_ev_data()
    print(ev)

#TODO create row in excel doc using pandas for each ev
print("done")
time.sleep(1000)
driver.close()
