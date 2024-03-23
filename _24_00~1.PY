import sys
import time
import re
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

INSTAGRAM_EMAIL = "YOUR_EMAIL"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"
URL_FOR_INSTAGRAM = "https://www.instagram.com/"

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def login_instagram(driver, email, password):
    driver.get(URL_FOR_INSTAGRAM)
    time.sleep(5)

    # Layered Catch Mechanism for locating the username field
    selectors = [
        (By.NAME, "username"),
        (By.XPATH, "//input[@aria-label='Phone number, username, or email']"),
        (By.CLASS_NAME, "_aa4b"),
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input"),
        (By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"),
        (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
    ]

    username_field = None
    for by, value in selectors:
        try:
            username_field = driver.find_element(by, value)
            if username_field:
                break
        except NoSuchElementException:
            continue

    if username_field is None:
        raise Exception("Username field not found after trying all selectors.")

    username_field.send_keys(email)
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    time.sleep(2)

    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

login_instagram(driver, INSTAGRAM_EMAIL, INSTAGRAM_PASSWORD)
