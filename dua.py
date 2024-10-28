from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("http://192.168.1.1")

username = "superadmin"
password = "suportadmin"

driver.find_element("id", "Frm_Username").send_keys(username)


# find password input field and insert password as well
driver.find_element("id", "Frm_Password").send_keys(password)
# click login button
driver.find_element("id", "LoginId").click()
# wait the ready state to be complete
# 5. Wait for the post-login page to load
WebDriverWait(driver, 10).until(
    EC.url_to_be("http://192.168.1.1/start.ghtml")
)

# 6. Extract the password element
password_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/table[2]/tbody/tr[5]/td[2]/input")

# 7. Access the password value (if needed)
password_value = password_element.get_attribute("value")

# 8. Print the extracted password value (optional)
print("Extracted password value:", password_value)

# 9. Close the browser
driver.quit()
