from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import os
import re
import json

configFile = open("config.json","r").read()
config = json.loads(configFile)

dataPath = "--user-data-dir=" + config['chromeDataPath']
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument(dataPath)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--lang=en-GB,en-US,en")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

#print(driver.execute_script("return navigator.userAgent;"))

#get videos from file
videos = []
tag = input("Enter tag: ")

tic = time.perf_counter()
driver.get(f"https://www.tiktok.com/tag/{tag}")

try:
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"css-wjuodt-DivVideoFeedV2 ecyq5ls0")]'))
    )
    toc = time.perf_counter()
    #print(f"Page Loaded in {toc-tic:0.4f} seconds")
except:
    print("Page Failed")
    driver.get_screenshot_as_file(os.curdir + "\\failed1.png")
    time.sleep(0.5)
    driver.get_screenshot_as_file(os.curdir + "\\failed2.png")

time.sleep(5)

htmlSource = str(driver.page_source)
links = [m.start() for m in re.finditer('https://www.tiktok.com/@', htmlSource)]
seen = []
for i in range(len(links)):
    link = htmlSource[links[i]:htmlSource.find('"',links[i])]
    video = "https://www.tiktok.com/@" + link 
    if video not in seen:
        seen.append(video)

with open("comments.txt","wb") as f:
    for video in seen:
        tic = time.perf_counter()
        driver.get(video)

        try:
            element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"DivCommentBarContainer")]'))
            )
            toc = time.perf_counter()
            print(f"Page Loaded in {toc-tic:0.4f} seconds")
        except:
            print("Page Failed")
            driver.get_screenshot_as_file(os.curdir + "\\failed1.png")
            time.sleep(0.5)
            driver.get_screenshot_as_file(os.curdir + "\\failed2.png")
            driver.quit()


        #Now we have the page loaded, we can get the comments from this div class css-g6odvl-DivCommentContainer ekjxngi0
        #comments = driver.find_elements(By.XPATH,'//div[contains(@class,"DivCommentListContainer")]')
        #get children of this div
        #parent = comments[0]
        children = driver.find_elements(By.XPATH,'.//div[contains(@class,"DivCommentItemContainer")]')
        #foreach child, get the username and comment
        f.write(("\n").encode('utf-8'))
        f.write(("Video: " + video + "\n").encode('utf-8'))
        f.write(("Comments:\n").encode('utf-8'))

        for i in range(len(children)):
            child = children[i]
            #print(child.find_elements(By.XPATH,'.//span[contains(@class,"SpanUserNameText")]')[0].text + ":")
            #print(child.find_elements(By.XPATH,'.//p[contains(@class,"PCommentText")]')[0].text)
            #print("--------------------")
            f.write((child.find_elements(By.XPATH,'.//span[contains(@class,"SpanUserNameText")]')[0].text + ":\n").encode('utf-8'))
            f.write((child.find_elements(By.XPATH,'.//p[contains(@class,"PCommentText")]')[0].text + "\n").encode('utf-8'))
            f.write(("--------------------\n").encode('utf-8'))
