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
from tqdm import tqdm

# --- CONFIG SETTINGS ---

# Load the config file (only contains the chrome data path for now)
configFile = open("config.json","r").read()
config = json.loads(configFile)
dataPath = "--user-data-dir=" + config['chromeDataPath']

# Define options for the Chrome Driver
options = Options()
options.add_argument("--window-size=1920,1200") # Set the window size
options.add_argument(dataPath) # Set the user data directory (to keep the user logged in on TikTok)

# Stanard options (Helps to make the program look less like a bot)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--lang=en-GB,en-US,en")
options.add_argument("--log-level=3") # Set the log level to 3 to stop the console from being spammed from the warnings - It will only show errors

# Create the Chrome Driver
driver = webdriver.Chrome(options=options)

# Define the user agent of the bot (Helps to make the program look less like a bot)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

# The stealth module is an extra measure to make this look less like a bot
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# --- END OF CONFIG SETTINGS ---



videos = []

# Get the tag from the user
tag = input("Enter tag: ")
print("Loading Tag...")

driver.get(f"https://www.tiktok.com/tag/{tag}")

try:
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"css-wjuodt-DivVideoFeedV2 ecyq5ls0")]'))
    )
except:
    # If the page fails to load, take a screenshot and close the program
    print("Page Failed")
    driver.get_screenshot_as_file(os.curdir + "\\failed1.png")
    time.sleep(0.5)
    driver.get_screenshot_as_file(os.curdir + "\\failed2.png")
    driver.quit()
    exit(1)

time.sleep(5)

htmlSource = str(driver.page_source)
links = [m.start() for m in re.finditer('https://www.tiktok.com/@', htmlSource)]
seen = []

# Get the links to the videos - It will find each link twice so duplicates will be removed
for i in range(len(links)):
    link = htmlSource[links[i]:htmlSource.find('"',links[i])]
    video = "https://www.tiktok.com/@" + link 
    if video not in seen:
        seen.append(video)


print("Loading Comments...")

with open("comments.txt","wb") as f:
    for video in tqdm(seen):
        tic = time.perf_counter()
        driver.get(video)

        try:
            element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"DivCommentBarContainer")]'))
            )
            toc = time.perf_counter()
            #print(f"Page Loaded in {toc-tic:0.4f} seconds")
        except:
            print("Page Failed")
            driver.get_screenshot_as_file(os.curdir + "\\failed1.png")
            time.sleep(0.5)
            driver.get_screenshot_as_file(os.curdir + "\\failed2.png")
            driver.quit()


        #Now we have the page loaded, we can get the comments from this div class css-g6odvl-DivCommentContainer ekjxngi0
        #with open("debug.txt","ab") as f:
        #    f.write(driver.page_source.encode('utf-8'))

        children = driver.find_elements(By.XPATH,'.//div[contains(@class,"DivCommentItemContainer")]')
        while len(children) < 100:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            children = driver.find_elements(By.XPATH,'.//div[contains(@class,"DivCommentItemContainer")]')
        f.write(("\n").encode('utf-8'))
        f.write(("Video: " + video + "\n").encode('utf-8'))
        f.write(("Comments:\n").encode('utf-8'))
    
        #print(f"Video: {video} - Comments: {len(children)}")
        for i in range(len(children)):
            child = children[i]

            #f.write(((str(child.find_element(By.XPATH,'.//a[contains(@data-e2e,"comment-avatar-1")]').get_attribute('outerHTML')).split('href="/@')[1].split('"')[0]) + ":\n").encode('utf-8')) # This is the username
            f.write((child.find_elements(By.XPATH,'.//span[contains(@class,"SpanUserNameText")]')[0].text + ":\n").encode('utf-8')) # This is the display name
            f.write((child.find_elements(By.XPATH,'.//p[contains(@class,"PCommentText")]')[0].text + "\n").encode('utf-8'))
            #f.write(((str(child.find_element(By.XPATH,'.//p[contains(@data-e2e,"comment-level-1")]').get_attribute('innerHTML'))).split('<span dir="">')[1].split('</span')[0] + "\n").encode('utf-8')) # This is the comment (More reliable)
            f.write(("--------------------\n").encode('utf-8'))
