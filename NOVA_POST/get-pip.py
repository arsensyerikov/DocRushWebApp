from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Шлях до драйвера (наприклад, ChromeDriver)
driver_path = "/Users/arsensyerikov/Documents/Python/NOVA_POST/chromedriver"


# Створюємо об'єкт служби для драйвера
service = Service(driver_path)

# Створюємо об'єкт браузера (наприклад, Chrome)
driver = webdriver.Chrome(service=service)

# Відкриваємо веб-сторінку
driver.get("https://new.novaposhta.ua/dashboard/invoices-my")
time.sleep(1)

# Увійти
button = driver.find_element(By.CLASS_NAME, "mat-menu-trigger")
button.click()
time.sleep(1)

# Приватна особа
driver.get("https://new.novaposhta.ua/auth/login-private-personhttps://new.novaposhta.ua/auth/login-private-person")
time.sleep(1)


#time.sleep(1)  # Зачекаємо, поки форма з'явиться або відновиться

# Телефон


driver.quit()










































#search_box = driver.find_element(By.NAME, 'q')
#search_box.send_keys("facebook")
#time.sleep(2)
#search_button = driver.find_element(By.CLASS_NAME, "gNO89b")
#search_button.click()
#time.sleep(2)
#result = driver.find_element(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
#result.click()
#time.sleep(2)




# Закриваємо браузер
