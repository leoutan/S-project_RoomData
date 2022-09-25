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
  #定位地點並輸入墾丁
  place = browser.find_element(By.XPATH,'//input[@aria-label="輸入城市、區域、景點或住宿名稱..."]')
  place.send_keys(u'墾丁')
  
  #等到下拉選單出現，就點選第一項地點
  first = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//li[@class='Suggestion Suggestion__categoryName']"))
  )
  first.click()
  time.sleep(2)
  #select_dates = browser.find_element(By.XPATH,"//div[@data-selenium='checkInBox']")
  #select_dates.click()

  #點選地點的下拉選單後，等到地點的下拉選單消失
  #網頁會自動跑出日曆，就能定位到入住日期，不必自己點選日曆
  #接著點選入住日期19號
  start_date = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH,"//div//*[text()='19']"))
  )
  start_date.click()

  #退房日期23號
  #因為elements用複數，click()前面加陣列選取第二項
  end_date = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located((By.XPATH,"//div//*[text()='23']"))
  )
  end_date[0].click()

  #如果選擇人下拉選單自己跳出來就執行finally
  #如果選單沒出現就執行except
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

time.sleep(10)
lists = WebDriverWait(browser, 10).until(
  EC.presence_of_element_located((By.XPATH,'//h3[@class="PropertyCard__HotelName"]'))
)
result_url = browser.current_url
#print(result_url)
#response = requests.get(result_url)
soup = BeautifulSoup(browser.page_source, 'html5lib')
js = "window.scrollTo(0, document.body.scrollHeight);"
browser.execute_script(js)
HotelNames = soup.find_all('h3', class_='PropertyCard__HotelName')
#print(soup)
for HotelName in HotelNames:
  print(HotelName.get_text())  