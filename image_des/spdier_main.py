from selenium import webdriver
import time,json
from selenium.webdriver.common.action_chains import ActionChains

#firefox = webdriver.Firefox()

profileDir = 'C:/Users/monster/AppData/Roaming/Mozilla/Firefox/Profiles/zi1rtobp.default'

profile = webdriver.FirefoxProfile(profileDir)

firefox = webdriver.Firefox(profile)

firefox.get('http://www.baidu.com')

firefox.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[3]/a[7]').click()
time.sleep(2)
firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()
time.sleep(2)

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').clear()
firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys('缺爱的山头')

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').clear()
firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys('luo8412098')

time.sleep(2)

firefox.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()

time.sleep(3)
js = "window.open('http://index.baidu.com/?tpl=trend&word=%BA%AB%B9%FA%C2%C3%D3%CE')"
firefox.execute_script(js)
time.sleep(2)
handles = firefox.window_handles
for handle in handles:# 切换窗口
    if handle != firefox.current_window_handle:
        firefox.close() # 关闭第一个窗口
        firefox.switch_to.window(handle) #切换到第二个窗口
# firefox.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[1]/div/div[2]/form/input[3]').clear()
# firefox.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[1]/div/div[2]/form/input[3]').send_keys('韩国旅游')

# firefox.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[1]/div/div[2]/div/span').click()

time.sleep(2)
print(firefox.title)
with open('s.txt','w+',encoding='utf-8') as f:
    f.write(firefox.page_source)


firefox.maximize_window()
firefox.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
firefox.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
firefox.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#2011']").click()
firefox.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
firefox.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#01']").click()
# 选择网页上的截止日期
firefox.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
firefox.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#2011']").click()
firefox.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
firefox.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#01']").click()
firefox.find_element_by_xpath("//input[@value='确定']").click()

xoyelement = firefox.find_elements_by_css_selector("#trend rect")[2]
x_place = 1

for i in range(20):
    ActionChains(firefox).move_to_element_with_offset(xoyelement,x_place, 50).perform()
    time.sleep(5)
    x_place += 20.5


