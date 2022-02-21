from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 동적 페이지에 대해 셀레니움으로 처리하기
# - 크롬 안띄우고 처리해보기(headless chrome : Chrome without Chrome)

appNum = 0


def howManyApp(web):
    global appNum
    soup = BeautifulSoup(web.page_source, 'lxml')
    now = len(soup.find_all('li', attrs={'class': 'ii-row media'}))
    if now == appNum:
        return False
    else:
        appNum = now
        print(appNum)
        return now


def google_movie_headless():
    ## 크롬 띄우고 처리할 경우 아래를 주석 처리 -----------------------
    # options = webdriver.ChromeOptions()
    # options.headless = True  # 크롬 안띄우기
    # options.add_argument('window-size=1920x1080')  # 윈도우 창 크기 지정
    # browser = webdriver.Chrome('./chromedriver.exe', options=options)
    # 여기까지 주석 처리 -------------------------------------------

    browser = webdriver.Edge('./msedgedriver.exe')  # 크롬 띄울 경우 주석 처리 풀기
    browser.maximize_window()
    url = 'https://fnd.io/#/kr/search?mediaType=ios&term=123456'
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'media-list')))

    soup = BeautifulSoup(browser.page_source, 'lxml')
    global appNum
    appNum = len(soup.find_all('li', attrs={'class': 'ii-row media'}))
    # 페이지에서 스크롤을 가장 아래로 내림
    for i in range(6):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        soup = BeautifulSoup(browser.page_source, 'lxml')
        while not howManyApp(browser):
            time.sleep(0.1)

    print('스크롤 완료')
    print(appNum)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    appList = soup.find_all('li', class_='ii-row media')
    title = appList[0].div.div.div.a
    print(title)
    input()
    print(soup.prettify())


google_movie_headless()