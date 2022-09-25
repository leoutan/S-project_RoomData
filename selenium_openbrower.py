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

#瀏覽網頁
url = 'https://www.agoda.com/?cid=1844104'
browser.get(url)
location = u'墾丁'

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
  place.send_keys(location)
  
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

#透過方向鍵下，讓頁面一直下移直到傳回的scrollTop值與前一次相同
#action = ActionChains(browser)
times, pages = 0, 0
while True:
  #判斷是否有搜尋到符合的房源，沒有的話就不向下滾動
  soup = BeautifulSoup(browser.page_source, 'html5lib')
  NoResult = soup.select('div.zero-page')
  if len(NoResult) >0:
    break
  #向下滾動每次500像素
  loc1 = browser.execute_script("return document.documentElement.scrollTop;")
  browser.execute_script("window.scrollBy(0, 500);")
  time.sleep(3)
  loc2 = browser.execute_script("return document.documentElement.scrollTop;")
  print(f"{loc1}=={loc2}")
  #滾動到最底讀取網頁資料
  if loc1 == loc2:
    HotelsName, HotelsRate, HotelsPrice = [], [], []
    pages+=1
    soup = BeautifulSoup(browser.page_source, 'html5lib')
    #print(soup.find_all('li', class_='PropertyCard PropertyCardItem'))
    for step, Hotel in enumerate(soup.select('div.JacketContent.JacketContent--Empty')):
        #飯店名稱
        try:
            if len(Hotel.select('h3')[0]) > 0:
                HotelsName.append(Hotel.select('h3')[0].get_text())
                #print(Hotel.select('h3')[0].get_text())
        except:
            HotelsName.append('0')
            #print('0')
        #飯店評分
        try:
            if len(Hotel.select('div.Box-sc-kv6pi1-0.ggePrW')[0]) != 0:
                HotelsRate.append(float(Hotel.select('div.Box-sc-kv6pi1-0.ggePrW')[0].get_text()))
                #print(Hotel.select('div.Box-sc-kv6pi1-0.ggePrW')[0].get_text())
        except:
            OtherMessage = Hotel.select('[data-element-name="new-to-agoda-badge"]')
            HotelsRate.append(OtherMessage[0].get_text())
            #print('0')
        #飯店價格
        #抓取到的價格會有千分號，直接轉int會錯誤，用replace去掉千分號
        try:
            if len(Hotel.select('span.PropertyCardPrice__Value')[0]) > 0:
                HotelsPrice.append(int(Hotel.select('span.PropertyCardPrice__Value')[0].get_text().replace(',','')))
                #print(Hotel.select('span.PropertyCardPrice__Value')[0].get_text())
        #沒有房間就不會出現價格，就以NoSales取代
        except:
            HotelsPrice.append('NoSales')
            #print('0')
    #左右合併飯店名稱、房價、評分
    df = pd.concat([pd.DataFrame(HotelsName),
                    pd.DataFrame(HotelsPrice),
                    pd.DataFrame(HotelsRate)], axis=1)
    df.columns=['HotelsName', 'HotelsPrice', 'HotelsRate']
    #每個迴圈透過golbals()宣告一個全域變數 P?，?由變數pages決定，每回圈加一
    # 所以第一圈會宣告P1，第二圈P2，依此類推
    #並同時把該頁的DataFrame表格丟入該迴圈變數中
    globals()['P'+str(pages)] = df
    print(f'Page{pages}')
    print(df)
    #寫入csv檔，mode='a'代表寫入同一檔案不會覆蓋上一次的資料
    #df.to_csv("D:\Privation\DS_notebook\專案\OUTPUT\\456.csv", encoding='utf_8_sig', mode='a')
        

    try:
        NextPage = WebDriverWait(browser,5).until(
        EC.presence_of_element_located((By.ID,'paginationNext'))
        )
        NextPage.click()
    except:
        print('This is last Page')
        break
#寫入excel檔，分不同工作表
#不能將下面code碼放到while迴圈內，每次寫入會把前面資料覆蓋
#必須把每個迴圈的變數P1、P2...，一次寫入
FileName = location + u'房源'
with pd.ExcelWriter(f"D:\Privation\DS_notebook\專案\OUTPUT\\{FileName}.xlsx") as writer:
    #以迴圈抓取每頁的表格寫入不同的工作表
    for p in range(0, pages):
      p+=1
      globals()['P'+str(p)].to_excel(writer, sheet_name=f"Page{p}")