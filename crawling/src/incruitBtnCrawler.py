from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time

chromedriver = "/Users/nahyeonan/Downloads/chromedriver"

# options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
# options.add_argument('disable-gpu')  # GPU 사용 안함
# options.add_argument('lang=ko_KR')  # 언어 설정
# driver = webdriver.Chrome(chromedriver, options=options)
driver = webdriver.Chrome(chromedriver)

driver.get("https://people.incruit.com/")
time.sleep(1)

driver.find_element_by_xpath('//*[@id="gnb_login"]/button').click()
driver.find_element_by_name('txtUserID').send_keys('gksk144@naver.com')
driver.find_element_by_name('txtPassword').send_keys('124wjd356!')
driver.find_element_by_xpath('//*[@id="g_form_login_box"]/fieldset/div/button').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="ResumeMainInfoLayer"]/div[1]/button').click()
driver.find_element_by_xpath('//*[@id="incruit_contents"]/div/div[5]/div[1]/div[1]/h4/a').click()

driver.switch_to.window(driver.window_handles[-1])

# 현재 인크루트 149페이지까지 합격 자소서 존재
# 11 page 중반부터 크롤링 필요
# 68 부터
for i in range(143, 150):
    print("================== page "+str(i)+" ==================")
    try:
        driver.get( "https://people.incruit.com/resumeguide/pdslist.asp?page="+str(i)+"&listseq=1&sot=&pds1=1&pds2=11&pds3=&pds4=&schword=&rschword=&lang=&price=&occu_b_group=&occu_m_group=&occu_s_group=&career=&pass=Y&compty=&rank=&summary=&goodsty=" )
    except NoSuchElementException:
        continue
    time.sleep(1)

    for j in range(1, 25):
        # //*[@id="incruit_contents"]/div/div[7]/table/tbody/tr[4]/td[2]/a
        driver.find_element_by_xpath('//*[@id="incruit_contents"]/div/div[7]/table/tbody/tr['+str(j)+']/td[2]/a').click()
        try:
            driver.find_element_by_xpath('//*[@id="section_brief_info"]//div[contains(@class, "shareWrap")]//button[contains(@class, "bbs_btn_download_mini")]').click()
        except NoSuchElementException:
            print("no download button : page {}, {} th resume".format(i, j))
            pass

        # check alert
        try:
            alert = driver.switch_to.alert
            alert.accept()
            continue
        except NoAlertPresentException:
            pass

        driver.back()

driver.quit()