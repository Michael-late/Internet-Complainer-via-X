import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time


class Xcomplain:
    def __init__(self):
        load_dotenv()
        self._email = os.getenv("twitter_email")
        print(self._email)
        self._password = os.getenv("twitter_password")
        self.promised_up = 10
        self.promised_down = 100
        self.okla_url = "https://www.speedtest.net/"
        self.x_url = "https://x.com/"
        
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        self.chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        
    def get_internet_speed(self):
        self.driver.get(url=self.okla_url)
        try:
            consent_btn = self.driver.find_element(By.ID,"onetrust-accept-btn-handler")
            print(consent_btn.text)
            consent_btn.click()
        except NoSuchElementException:
            pass
        start_test = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.js-start-test")))
        start_test.click()
        time.sleep(20)
        self.result_down = self.driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        time.sleep(20)
        self.result_up = self.driver.find_element(By.CSS_SELECTOR,".upload-speed").text
        print(self.result_up) 
        
    def close(self):
        self.driver.close()
    
    def login(self):
        try:
            self.driver.get(self.x_url)
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
            login_btn.click()
            time.sleep(1)
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
            username_input.send_keys(self._email)
            username_input.send_keys(Keys.ENTER)
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[autocomplete='current-password']")
            password_input.send_keys(self._password)
            password_input.send_keys(Keys.ENTER)
        except:
            pass
    
    def complain(self):
        time.sleep(8)
        text_box = self.driver.find_element(By.CSS_SELECTOR,"br[data-text='true']")
        # text_box.send_keys(f"{self.result_down} down & {self.result_up} up")
        text_box.send_keys("1")        
        
        time.sleep(3)
        post_btn = self.driver.find_element(By.CSS_SELECTOR,'button[data-testid="tweetButtonInline"]')
        post_btn.click()
    
X = Xcomplain()
X.login()
X.complain()
# X.get_internet_speed()
# if float(X.result_down) < 100 or float(X.result_up) < 10:
#     X.login()
#     X.complain()
# else:
#     print("GOOD")