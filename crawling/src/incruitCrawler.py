from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

chromedriver = "/Users/nahyeonan/Downloads/chromedriver"

driver = webdriver.Chrome(chromedriver)
driver.get("https://people.incruit.com")
time.sleep(1)

driver.find_element_by_id('gnb_login').click()
driver.find_element_by_name('txtUserID').send_keys('gksk144@naver.com')
driver.find_element_by_name('txtPassword').send_keys('124wjd356!')
driver.find_element_by_xpath('//*[@id="g_form_login_box"]/fieldset/div/button').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="ResumeMainInfoLayer"]/div[1]/button').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="incruit_contents"]/div/div[5]/div[1]/div[1]/h4/a').click()

driver.switch_to.window(driver.window_handles[-1])

resume_links = []
saving_path = "../../datafiles/raw-data/incruit-dom/"
basic_addr = "https://people.incruit.com/resumeguide"

for i in range(1, 12):
    href = 'https://people.incruit.com/resumeguide/pdslist.asp?page=' + str(i) + '&pds1=1&pds2=11&pass=y'
    driver.get(href)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print("======== "+str(i)+" ========")
    for j in range(1, 25):
        img = soup.select("#incruit_contents > div > div.bbsWrap > table > tbody > tr:nth-child(" + str(j) \
                          + ") > td:nth-child(6) > img")
        if len(img) != 0:
            print("{}페이지 {}번째부터는 파일 다운로드 필요".format(i, j))
            break

        filename = "incruit-" + str(i) + "-" + str(j) + '.txt'
        f = open(saving_path + filename, 'wt')

        link = soup.select("#incruit_contents > div > div.bbsWrap > table > tbody > tr:nth-of-type(" + str(j) \
                           + ") > td:nth-of-type(2) > a")

        req = requests.get(basic_addr + link[0].attrs['href'][1:])
        text = req.text

        f.write(text)
        f.close()

    time.sleep(1)

driver.quit()