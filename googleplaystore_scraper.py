from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

app_list = []  # 앱 이름 리스트
id_list = []  # 링크 리스트
app_info = []  # 상세정보

interval = 2

driver = webdriver.Chrome('./chromedriver')
driver.get(
    'https://play.google.com/store/apps/collection/cluster?clp=0g4jCiEKG3RvcHNlbGxpbmdfZnJlZV9BUFBMSUNBVElPThAHGAM%3D:S:ANO1ljKs-KA&gsr=CibSDiMKIQobdG9wc2VsbGluZ19mcmVlX0FQUExJQ0FUSU9OEAcYAw%3D%3D:S:ANO1ljL40zU&hl=ko&gl=US')

page_height = driver.execute_script("return document.body.scrollHeight")  # 페이지 높이 저장
# print(page_height)

# 화면 맨 아래로 스크롤하도록 구현
while True:
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight)")  # 현재 페이지에서 맨 아래로 스크롤 내리기 (아마 해상도 높이 만큼 내려갈걸)
    time.sleep(interval)  # 2초동안 페이지 로딩 대기

    curr_height = driver.execute_script("return document.body.scrollHeight")  # 현재 페이지 높이 저장
    if curr_height == page_height:
        break

    page_height = curr_height

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
# name=soup.select("div.WsMG1c.nnK0zc")#앱이름
# rating = soup.select('div.pf5lIe > div') #별점
# ratenum= soup.select('span.sT93pd CKzsaf > span.w2kbF') #앱리뷰수
# detail= soup.select('span.sT93pd CKzsaf > span.w2kbF') #앱 상세설명
code = soup.select("div.b8cIId.ReQCgd.Q9MA7b > a")

for i in code:
    app_list.append(i.text)
    id = i.attrs["href"]
    id_list.append(id[23:])

for a in id_list:
    info = app(
        a,
        lang='ko',
        country='us')
    del info['comments']
    app_info.append(info)

# driver.quit()

df = pd.DataFrame({'App name': app_list, 'App id': id_list})  # 리스트를 데이터 프레임으로 합쳐주기
df1 = pd.concat([df], ignore_index=True)
df2 = pd.DataFrame(app_info)
result = pd.concat([df1, df2], axis=1)
print(result)