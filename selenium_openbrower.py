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

#開啟Chrome瀏覽器
browser = webdriver.Chrome(ChromeDriverManager().install())

#瀏覽網頁
url = 'https://www.agoda.com/?cid=1844104'
browser.get(url)

#如果10秒內出現優惠廣告，定位點擊XX按鈕，再執行finally
#10秒後沒出現廣告則直接執行finally
try:
  close = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.XPATH,"//button[@class='ab-close-button']"))
  )
  close.click()

finally:
  #定位地點
  place = browser.find_element(By.XPATH,'//input[@aria-label="輸入城市、區域、景點或住宿名稱..."]')
  place.send_keys(u'墾丁')
  
  first = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[@class='Suggestion Suggestion__categoryName']"))
  )
  first.click()
  time.sleep(2)
  #select_dates = browser.find_element(By.XPATH,"//div[@data-selenium='checkInBox']")
  #select_dates.click()



  start_date = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH,"//div//*[text()='19']"))
  )
  start_date.click()
  end_date = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.XPATH,"//div//*[text()='23']"))
  )
  end_date[1].click()
  try:
    Select_traveller = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@class="Traveller"]'))
    )
  except:
    Select_traveller = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@data-selenium="occupancyBox"]'))
    )
    Select_traveller.click()
  finally:
    travellers = WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH,'//div[@data-selenium="traveler-solo"]'))
    )
    travellers.click()
  search = browser.find_element(By.XPATH, '//button[@data-selenium="searchButton"]')
  search.click()
  dont = WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.XPATH,'//span[text()="不用了"]'))
  )
  dont.click()

result_url = browser.current_url

    