from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import time
import pickle
import gspread
from google.oauth2.service_account import Credentials

CHROME_DRIVER_PATH = "chromedriver-win64/chromedriver.exe"
EMAIL = "pratikranjan240924@gmail.com"
PASSWORD = "y/5B*#@X#!N;a-"
COOKIES = "cookies/COOKIES_ACCOUNT_1.pkl"
SERVICE = Service(CHROME_DRIVER_PATH)
DRIVER = webdriver.Chrome(service=SERVICE)

json_key_file = 'aster-sheet-key.json'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(json_key_file, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Linkedin-connections").sheet1


def login_cookies(email, password, cookie_path):

    DRIVER.get("https://www.linkedin.com/login")

    try:
        cookies = pickle.load(open(cookie_path, "rb"))
        for cookie in cookies:
            DRIVER.add_cookie(cookie)
        print("Loaded Cookies")
        time.sleep(5)
        DRIVER.refresh()
        time.sleep(5)

    except Exception as e:
        print(f"Error loading cookies: {e}")
        print("Logging in with email and password...")
        email_field = DRIVER.find_element("id", "username")
        email_field.send_keys(email)    
        password_field = DRIVER.find_element("id", "password")
        password_field.send_keys(password) 
        password_field.send_keys(Keys.RETURN)
        time.sleep(50)
        cookies = DRIVER.get_cookies()
        pickle.dump(cookies, open(cookie_path, "wb"))
        print("Cookies saved for future use.")

    time.sleep(5)

def get_connections():

    print("entered  get connections")

    data = []
    DRIVER.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
    sleep(10)
    html_content = DRIVER.page_source

    with open('page_content.html', 'w', encoding='utf-8') as file:
        file.write(html_content)


    connections = DRIVER.find_elements("css selector", 'li.mn-connection-card')
    sleep(5)
    print(connections)
    for connection in connections:

        name_tag = connection.find_element("css selector", 'span.mn-connection-card__name')
        name = name_tag.text.strip() if name_tag else None
        # print(name)

        url_tag = connection.find_element("css selector", 'a.mn-connection-card__link')
        url = f"https://www.linkedin.com{url_tag.get_attribute('href')}" if url_tag else None
        # print(url)

        occupation_tag = connection.find_element("css selector", 'span.mn-connection-card__occupation')
        occupation = occupation_tag.text.strip() if occupation_tag else None
        # print(occupation)
        # print(name, url, occupation)
        # data.append([name, url, occupation])
        writetosheet(name, url, occupation)
    # for row in data:
    #     print(row)
def writetosheet(name,url,occupation):
    existing_urls = sheet.col_values(3)
    if url not in existing_urls:

        sheet.append_row([name, occupation, url])
        print(f"New data for {name} appended to Google Sheet!")
    else:
        print(f"{url} already exists in Google Sheet. Skipping duplicate entry.")


login_cookies(email=EMAIL, password=PASSWORD, cookie_path=COOKIES) 
get_connections()