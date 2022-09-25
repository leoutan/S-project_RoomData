from email.utils import localtime
import imp
from numpy import broadcast
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#開啟Chrome瀏覽器
browser = webdriver.Chrome(ChromeDriverManager().install())

try:
    Select_traveller = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@class="Traveller"]'))
    )

  #點選旅遊人數跑出下拉選單
except:
    Select_traveller = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@data-selenium="occupancyBox"]'))
    )
    Select_traveller.click()

  #從下拉選單中選擇單人旅遊
finally:
    travellers = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@data-selenium="traveler-solo"]'))
    )
    travellers.click()
  
  #定位並點選搜尋按鈕
search = browser.find_element(By.XPATH, '//button[@data-selenium="searchButton"]')
search.click()
dont = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.XPATH,'//span[text()="不用了"]'))
  )
dont.click()
'''
test002
'''