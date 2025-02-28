from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#driver_path = "/Users/arsensyerikov/Documents/Python/NOVA_POST/chromedriver"

#service = Service(driver_path)

# Створюємо об'єкт браузера (наприклад, Chrome)
driver = webdriver.Chrome()

driver.get(" https://new.novaposhta.ua/auth/login-private-person")
time.sleep(1)

phone_input = driver.find_element(By.ID, "mat-input-0")
phone_input.send_keys("502819686")
time.sleep(1)


submit_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Далі')]]")
submit_button.click()
time.sleep(200)

password_input = driver.find_element(By.ID, "f_8ac95141-16f7-4a25-bc83-9fa8a0d98dd3")
password_input.send_keys("130210")
time.sleep(1)

continue_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Продовжити')]")
continue_button.click()
time.sleep(1)
time.sleep(100)
driver.quit()