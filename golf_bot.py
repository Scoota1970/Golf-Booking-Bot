import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PREFERRED_TIME = 9*60  # minutes

def second_friday(date):
    return date.weekday() == 4 and (date.day-1)//7 % 2 == 0

target = datetime.date.today() + datetime.timedelta(days=8)

if not second_friday(target):
    print("Not a booking day")
    exit()

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("https://collierpark.miclub.com.au")

time.sleep(5)

# login
username = os.environ["GOLF_USER"]
password = os.environ["GOLF_PASS"]

driver.find_element(By.ID,"username").send_keys(username)
driver.find_element(By.ID,"password").send_keys(password)
driver.find_element(By.ID,"login").click()

time.sleep(5)

driver.get("TEE_SHEET_PAGE")

while datetime.datetime.now().time() < datetime.time(12,0,1):
    time.sleep(0.1)

driver.refresh()

times = driver.find_elements(By.CLASS_NAME,"slot")

best=None
best_diff=9999

for t in times:

    txt=t.text
    h,m=map(int,txt.split(":"))
    mins=h*60+m

    diff=abs(PREFERRED_TIME-mins)

    if diff < best_diff:
        best_diff=diff
        best=t

if best:
    best.click()

    driver.find_element(By.ID,"players").send_keys("4")
    driver.find_element(By.ID,"carts").send_keys("2")

    driver.find_element(By.ID,"confirmBooking").click()

print("Booking attempted")
