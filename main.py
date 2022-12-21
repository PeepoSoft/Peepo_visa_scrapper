from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
import sys
import json
from conf import username, password, url_id, country_code, city_id
import datetime
TIME = 60

BASE_URL = f'https://ais.usvisa-info.com/es-{country_code}/niv'
CITIES_BASE_URL = f'https://ais.usvisa-info.com/es-{country_code}/niv/schedule/{url_id}/appointment/days/'

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome(executable_path="C:\\Users\\Jassiel\\Documents\\Visa\\chromedriver.exe")

def search_in_json(data, city):   
    for date_item in data:
        date = date_item['date']
        v = date.split('-')
        v = list(map(int, v))
        is_business_day = date_item['business_day']
        if is_business_day:
            d1 = datetime.datetime(v[0], v[1] , v[2])
            d2 = datetime.datetime(2023, 6, 30)
            if d1 < d2: 
                print('Cita disponible el dia {} en la ciudad de {}'.format(date, city))
        
def log_in():
    print('Log in entered')
    if driver.current_url != BASE_URL + '/users/sign_in':
        print('We are logged!!!')
        get_dates()
        return
    print('Logging in...')
    
    try:
        # wait until /html/body/div[7]/div[3]/div/button is clickable
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/button'))
        # Clicking the 'X' button
        driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/button').click()
    except:
        pass

    try:
        #wait until /html/body/div[1]/a is clickable
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[1]/a'))
        # Clicking the 'X' button
        driver.find_element(By.XPATH, '/html/body/div[1]/a').click()
    except:
        pass
    
    user_box = driver.find_element(By.NAME, 'user[email]')
    user_box.send_keys(username)
    # time sleep to avoid bot detection
    time.sleep(2)
    password_box = driver.find_element(By.NAME, 'user[password]')
    password_box.send_keys(password)
    time.sleep(2)
    # Clicking the checkbox and wait until /html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div is clickable
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div'))
    driver.find_element(By.XPATH, '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div').click()
    time.sleep(2)
    # Clicking 'Sign in'
    # wait until commit is clickable
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input'))
    driver.find_element(By.XPATH, '/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input').click()
    time.sleep(2)
    print('Login successful... Getting dates')
    get_dates()
   

def get_dates():
     for city in city_id.keys():
        time.sleep(2)
        driver.get(CITIES_BASE_URL + '{}.json'.format(city))
        content = driver.find_element(By.XPATH, '/html/body/pre').text
        parsed_json = json.loads(content)
        print('Dates got successfully from', city_id[city])
        search_in_json(parsed_json, city)

def get_data():
    while True:
        try:
            driver.get(BASE_URL + f'/schedule/{url_id}/appointment')	
            log_in()
            break
        except ElementNotInteractableException:
            time.sleep(6)
def start():
    while True:
        get_data()
        time.sleep(TIME)

#start()
f = open('test.json')
data = json.load(f)
search_in_json(data, 'Guadalajara')