from selenium import webdriver
import time


firefox = webdriver.Firefox()

firefox.get('https://www.baidu.com')

firefox.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/a[7]').click()

time.sleep(1)

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()



firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys('缺爱的山头')

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys('luo8412098')

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()

#s = 'http://index.baidu.com/?tpl=trend&word=韩国旅游'

#s = s.encode('gb2312')

firefox.get('http://index.baidu.com/#/')

firefox.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[1]/div/div[2]/form/input[3]').send_keys('韩国旅游')

firefox.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[1]/div/div[2]/div/span/span').click()
