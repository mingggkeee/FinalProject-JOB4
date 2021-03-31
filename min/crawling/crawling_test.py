# print("hello~")

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time


#클립보드에 input을 복사한 뒤
#해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기
def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)


id = 'gksk144'
pw = '1234wjd5678'

driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(3)

driver.get("https://people.incruit.com/")
driver.find_element_by_xpath('//*[@id="gnb_login"]/button').click()
# driver.find_element_by_xpath('//*[@id="incruit_contents"]/div/div[5]/div[1]/div[1]/h4/a').click()
# driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

copy_input('//*[@id="id"]', id)
time.sleep(1)
copy_input('//*[@id="pw"]', pw)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()