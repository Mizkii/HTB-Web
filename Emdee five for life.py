#!/usr/bin/env python3
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import hashlib


green = '\033[92m'
red = '\033[91m'
end = '\033[0m'
    

parser = argparse.ArgumentParser()
parser.add_argument('-u', help='url', dest='url')

args = parser.parse_args()


def banner():
    print ('''%s
HTB
____ _  _ ___  ____ ____   %s ____ _ _  _ ____ %s   ____ ____ ____    _    _ ____ ____
|___ |\/| |  \ |___ |___   %s |___ | |  | |___ %s  |___ |  | |__/    |    | |___ |___
|___ |  | |__/ |___ |___   %s |    |  \/  |___ %s  |    |__| |  \    |___ | |    |____

-u for "URL"                                                                          
%s''' % (green, red, green, red, green, red, green, end))

banner()



if not args.url:
    print("please use - u for http://url")
else:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(args.url)
    for i in range(100):
        toHash = driver.find_element_by_css_selector('h3')
        html = toHash.get_attribute('innerHTML')
        inputbox = driver.find_element_by_css_selector('input')
        result = hashlib.md5(str(html).encode('utf-8'))
        ourHash = result.hexdigest()
        inputbox.send_keys(ourHash)
        inputbox.send_keys(Keys.ENTER)
        outhtml = driver.find_element_by_css_selector('p')
        out = outhtml.get_attribute('innerHTML')
        if (out.find('HTB') != -1):
            print(out)
            exit()
