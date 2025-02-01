import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .config_manager import Config


class Brow:
    def __init__(self, config: Config):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--disable-blink-features=AutomationControlled") 
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        self.login = config.mail
        self.password = config.password

    def __del__(self):
        self.driver.close()

    def auth(self):
        self.driver.get("https://lk.sut.ru/cabinet")
        elem = self.driver.find_element(By.NAME, "users")
        elem.clear()
        elem.send_keys(self.login)
        
        elem = self.driver.find_element(By.NAME, "parole")
        elem.clear()
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        
        elem = self.driver.find_element(By.NAME, "logButton")
        elem.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(6) # seconds
    
    def get_token(self):
        self.auth()
        token = self.driver.get_cookie("miden")["value"]
        time.sleep(0.25)
        return token
