from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import sys
import time
import pyperclip
import requests

# 저장 경로도 전달받아야 함
if sys.argv[1] is None or sys.argv[2] is None or sys.argv[3] is None:
    print("usage: python jobKoreaCrawler.py [own naver id] [own naver password] --os=<w or m>")
    print()
    print("===== Option =====")
    print("--os=<w or m>")
    print("\tw : window")
    print("\tm : mac os")
    sys.exit(1)

if len(sys.argv) > 4:
    print("too many arguments\n")
    print("usage: python jobKoreaCrawler.py [own naver id] [own naver password] --os=<w or m>")
    sys.exit(1)

if sys.argv[3] != '--os=w' and sys.argv[3] != '--os=m':
    print("os should be w (window) or m (mac os)")
    print()
    print("===== Option =====")
    print("--os=<w or m>")
    print("\tw : window")
    print("\tm : mac os")
    sys.exit(1)

user_id = sys.argv[1]
user_pw = sys.argv[2]
user_os = sys.argv[3][-1]

chromedriver = "/Users/nahyeonan/Downloads/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument('headless') 
options.add_argument('disable-gpu') 
options.add_argument('lang=ko_KR') 
driver = webdriver.Chrome(chromedriver, options=options)

# driver = webdriver.Chrome(chromedriver)
user_id = argv[1]
user_pw = argv[2]
user_os = argv[3][-1]


chromedriver = "/Users/nahyeonan/Downloads/chromedriver"

# options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
# options.add_argument('disable-gpu')  # GPU 사용 안함
# options.add_argument('lang=ko_KR')  # 언어 설정
# driver = webdriver.Chrome(chromedriver, options=options)

driver = webdriver.Chrome(chromedriver)
driver.get("https://www.jobkorea.co.kr/")
time.sleep(1)

# try:
driver.find_element_by_xpath("//button[@title='네이버 로그인']").click()
time.sleep(1)

driver.switch_to.window(driver.window_handles[-1])

id_elm = driver.find_element_by_id('id')
pw_elm = driver.find_element_by_id('pw')

id_elm.click()
pyperclip.copy(user_id)  # naver id = sys.argv[1]
if user_os == 'm':
    id_elm.send_keys(Keys.COMMAND, 'v')
else:
    id_elm.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

pw_elm.click()
pyperclip.copy(user_pw)  # naver pw = sys.argv[2]
if user_os == 'm':
    pw_elm.send_keys(Keys.COMMAND, 'v')
else:
    pw_elm.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

driver.find_element_by_xpath("//input[@id='log.login']").click()
time.sleep(1)
driver.close()

driver.switch_to.window(driver.window_handles[0])

driver.find_element_by_xpath("//div[@class='jkNavArea']/ul[1]/li[2]/a").click()
driver.find_element_by_xpath("//div[@class='starSideNav']/div[4]/ul/li[1]/a").click()
time.sleep(1)

# pop up 존재하는지 예외처리 필요
driver.find_element_by_xpath("//div[contains(@class, 'firstPopUp')]/div/button").click()

jobkorea = "https://www.jobkorea.co.kr"

while True:

    import re
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    todayTotal = soup.select("#container > div.stContainer > div:nth-child(4) > h4 > span:nth-child(2)")[0]
    nums = "".join(re.findall("\d+", todayTotal.contents[0]))
    todayTotal = int(nums)

    addrs = soup.select("div > .ctTarget")[0].select("ul.selfLists > li > a")
    cnt = len(addrs)

    pages = soup.select("div.tplPagination")[0].select("ul > li")

    print(pages)
    print(pages[0].select("span.now"))

    start_page = pages[0].select("span.now")[0].contents[0]
    start_page = int(start_page)

    print(start_page, start_page+len(pages))

    for j in range(start_page, start_page + len(pages)):
        try:
            driver.find_element_by_xpath("//*[@id='container']/div[2]/div[5]/div[2]/ul/li[" + str(j) + "]/a").click()
        except NoSuchElementException:
            pass

        for i in range(cnt):
            f = open('/Users/nahyeonan/ssac/proj1/job4/datafiles/test/jk-' + str(j) + "-" + str(i) + '.txt', 'wt')
            req = requests.get(jobkorea + addrs[i].attrs['href'])
            tex = req.text
            f.write(tex)
            f.close()

    try:
        driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[5]/div[2]/p').find_element_by_xpath("//a[contains(@class, 'btnPgnNext')]").click()
    except NoSuchElementException:
        print("no such element")
        sys.exit(1)
    except:
        print("error")

driver.quit()
