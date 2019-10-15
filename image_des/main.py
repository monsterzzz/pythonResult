from selenium import webdriver
import time,json
from selenium.webdriver.common.action_chains import ActionChains
import random
from PIL import Image
import os

class index_spider:
    def __init__(self,username = '缺爱的山头',password = 'luo8412098',kw='韩国旅游',start_date = '2011-01',end_date = '2018-07'):
        self.kw = kw
        self.start_date = start_date
        self.start_year = self.start_date.split('-')[0]
        self.start_month = self.start_date.split('-')[1]
        self.end_date = end_date
        self.end_year = self.end_date.split('-')[0]
        self.end_month = self.end_date.split('-')[1]
        self.username = username
        self.password = password
        self.move_time = 30
        self.driver = self.get_driver()
        self.one_flow()


    def get_driver(self):
        profileDir = 'C:/Users/monster/AppData/Roaming/Mozilla/Firefox/Profiles/zi1rtobp.default'
        profile = webdriver.FirefoxProfile(profileDir)
        firefox = webdriver.Firefox(profile)
        return firefox

    def login(self):
        firefox = self.driver
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

    def open_index_page(self):
        firefox = self.driver
        js = "window.open('http://index.baidu.com/?tpl=trend&word=%BA%AB%B9%FA%C2%C3%D3%CE')"
        firefox.execute_script(js)
        time.sleep(2)
        handles = firefox.window_handles
        for handle in handles:# 切换窗口
            if handle != firefox.current_window_handle:
                firefox.close() # 关闭第一个窗口
                firefox.switch_to.window(handle) #切换到第二个窗口

    def click_date(self,year,month):
        firefox = self.driver

        firefox.maximize_window()
        firefox.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
        firefox.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
        firefox.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#%s']" % str(year)).click()
        firefox.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
        firefox.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#%s']" % str(month)).click()
        # 选择网页上的截止日期
        firefox.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
        firefox.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#%s']" % str(year)).click()
        firefox.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
        firefox.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#%s']" % str(month)).click()
        firefox.find_element_by_xpath("//input[@value='确定']").click()

    def move_mouse(self,path_dir):
        def find_real_span(file_name):
            try:
                tag = firefox.find_element_by_xpath('//div[@id="viewbox"]')
                print(tag.location)
                print(tag.size)
                left = tag.location['x']
                top = tag.location['y']
                right = left + tag.size['width']
                bottom = top + tag.size['height']
                im = Image.open(file_name)
                im = im.crop((left, top, right, bottom))
                im.save(file_name)
            except BaseException as e:
                print(e)
                print('get attrib error')

        firefox = self.driver
        file_name = path_dir + '/%s.png'
        xoyelement = firefox.find_elements_by_css_selector("#trend rect")[2]
        real_x = 20
        x_place = 1
        for i in range(self.move_time):
            ActionChains(firefox).move_to_element_with_offset(xoyelement,x_place, 20).perform()
            x_place += 40.4666
        x_place = 1
        for i in range(self.move_time):
            ActionChains(firefox).move_to_element_with_offset(xoyelement,x_place, 20).perform()
            time.sleep(2)
            if self.ex_box():
                time.sleep(2)
                firefox.save_screenshot(file_name % str(i))
                find_real_span(file_name % str(i))
            else:
                cout = 0
                while True:
                    if cout >= 4:
                        break
                    ActionChains(firefox).move_to_element_with_offset(xoyelement, x_place - 40.46666/2, 10 ).perform()
                    for k in range(20):
                        if cout < 2 : 
                            ActionChains(firefox).move_to_element_with_offset(xoyelement, x_place - 40.46666/2 + k+1 , 5 ).perform()
                            if self.ex_box() and k >= 3:
                                time.sleep(1)
                                firefox.save_screenshot(file_name % str(i))
                                find_real_span(file_name % str(i))
                                cout = 4
                                break
                        else:
                            ActionChains(firefox).move_to_element_with_offset(xoyelement, x_place - 40.46666/2 - 5 + k+1 , 5 ).perform()
                            if self.ex_box() and k >= 8:
                                time.sleep(1)
                                firefox.save_screenshot(file_name % str(i))
                                find_real_span(file_name % str(i))
                                cout = 4
                                break
                    cout += 1
        
            time.sleep(1)
            x_place += 40.466
            real_x += 40.466
            print(real_x)

    

    def ex_box(self):
        firefox = self.driver
        try:
            tag = firefox.find_element_by_xpath('//div[@id="viewbox"]')
            print(tag.is_displayed())
            return tag.is_displayed()
        except:
            return False

    def one_flow(self):
        self.login()
        time.sleep(5)
        self.open_index_page()
        for i in range(int(self.start_year),int(self.end_year)+1):
            for k in range(int(self.start_month),13):
                if k == 2 :
                    if i == 2012 or i == 2016:
                        self.move_time = 29
                    else:
                        self.move_time = 28
                elif k == 1 or k == 3 or k == 5 or k == 7 or k == 8 or k == 10 or k == 12:
                    self.move_time = 31
                else:
                    self.move_time = 30
                if k < 10 :
                    k = '0%s' % k
                print('%s - % s ' % (str(i),str(k)))
                self.click_date(str(i),str(k))
                if not os.path.exists(os.getcwd() + '\\' + '%s_%s' % (str(i),str(k))):
                    os.mkdir(os.getcwd() + '\\' + '%s_%s' % (str(i),str(k)))
                self.move_mouse(os.getcwd() + '\\' + '%s_%s' % (str(i),str(k)))
                if i == int(self.end_year) and k == int(self.end_month):
                    break
                
    
    #def date_to(self):
        #os.mkdir(os.getcwd() + '\\' + '%s_%s' % (str(2011),str(1)))
        #print(os.path.exists(os.getcwd() + '\\' + '%s_%s' % (str(2011),str(1))))
        #print(os.getcwd() + '\\' + '%s_%s' % (str(2011),str(1)))
                

s = index_spider()
#s.date_to()