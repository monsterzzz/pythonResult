import requests
import json,time,pandas,os
from bs4 import BeautifulSoup

class Base_Tool:
    def make_header(self):
        header = {
            "Host": "lvyou.baidu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
            "Referer": "https://lvyou.baidu.com/hanguo/",
        }
        return header
    def save_msg(self,name,content):
        with open('test_dir/%s.txt' % name,'w+',encoding='utf-8') as f:
            f.write(str(content))

class node(Base_Tool):
    def __init__(self,url):
        self.url = url
        self.header = self.make_header()
        self.title = 'none'
        self.time = 'none'
        self.days = 'none'
        self.cost = 'none'
        self.from_to = 'none'
        self.dir = 'none'
        self.content = ''
        self.code = 'none'
        self.type = 'none'
        self.update_time = 'none'
        self.write_time = 'none'
        self.aut = 'none'
        print(self.url)
        self.run()


    def get_main_page(self):
        r = requests.get(self.url,headers=self.header)
        r.encoding = 'utf-8'
        print('node : ' + str(r.status_code))
        if r.status_code == 200:
            return r.text
        else:
            return ''


    def get_dir(self,string:str):
        s = BeautifulSoup(string,'lxml')
        try:
            dir_tag = s.find('ul',attrs={'id':'J-catalog-list'})
            list_tag = dir_tag.find_all('a')
            result = ''
            for i in list_tag:
                result += i.get_text(strip=True) + '\n'
            self.dir = result.replace('展开\n','')
        except:
            print('dir found error')
            self.code = 'dir found error'

    def get_floor_content(self,soup):
        s = soup
        content = ''
        try:
            floor_place_tag = s.find('p',attrs={'class':'places'})
            floor_place_tag_content = s.find('p',attrs={'class':'places'}).get_text(strip=True)
            floor_place_tag.decompose()
        except:
            floor_place_tag_content = ''
        try:
            floor_title = s.find('h4').get_text(strip=True)
            content += floor_title + '\n'
            content += floor_place_tag_content + '\n'
        except:
            pass
        try:
            real_content_tag = s.find('div',attrs={'class':'content'})
            P_list_tag = real_content_tag.find_all('p')
            for i in P_list_tag:
                if i.get_text(strip=True) != '':
                    content += i.get_text(strip=True) + '\n'
        except:
            print('content ERROR')
            self.code = 'content ERROR'
        
        return content

    def get_all_floor(self,string:str):
        s = BeautifulSoup(string,'lxml')
        try:
            self.write_time = s.find("span",attrs={'class':'time secondary'}).get_text(strip=True).replace('发表于：','')
        except:
            pass
        try:
            owner_content_tag = s.find('div',attrs={'id':'pagelet_main'}).find('ul',attrs={'class':'master-posts-list'})
            owner_content_floor = owner_content_tag.find_all('li')
            if len(owner_content_floor) == 14:
                for i in owner_content_floor:
                    c = self.get_floor_content(i)
                    self.content += c + '\n\n'   
                try:
                    page_list = s.find('div',attrs={'class':'view-ft clearfix'})
                    page = page_list.find_all('a')
                    floor_num = 15
                    for i in range(len(page)-1):
                        r = requests.get(self.url +'-'+ str(floor_num),headers=self.header)
                        print(self.url +'-'+ str(floor_num))
                        r.encoding = 'utf-8'
                        s = BeautifulSoup(r.text,'lxml')
                        owner_content_tag = s.find('div',attrs={'id':'pagelet_main'}).find('ul',attrs={'class':'master-posts-list'})
                        owner_content_floor = owner_content_tag.find_all('li')
                        if len(owner_content_floor) == 14:
                            for i in owner_content_floor:
                                c = self.get_floor_content(i)
                                self.content += c + '\n\n'  
                            floor_num += 15 
                        else:
                            for i in owner_content_floor:
                                c = self.get_floor_content(i)
                                self.content += c + '\n\n' 
                            break

                except:
                    print('deep page ERROR')
                    self.code = 'deep page ERROR'
            else:
                for i in owner_content_floor:
                    c = self.get_floor_content(i)
                    self.content += c + '\n\n'  
        except:
            pass
    def run(self):
        x = self.get_main_page()
        self.get_dir(x)
        self.get_all_floor(x)
    

class list_msg(Base_Tool):
    def __init__(self,page=1):
        self.header = self.make_header()
        self.page = 127
        

    def get_list(self,pn):
        url = 'https://lvyou.baidu.com/search/ajax/search?format=ajax&sid=d7e376b3690f23d1dc24bbfb&word=韩国&ori_word=韩国&father_place=亚洲&pn=%s&rn=6' % str(pn)
        r = requests.get(url,headers=self.header)
        print(r.status_code)
        pydic = json.loads(r.text)
        if pydic['errno'] == 0:
            return pydic['data']['search_res']['notes_list']
        else:
            return {}

    def iter(self,l:list):
        title = []
        url = []
        write_time = []
        times = []
        days = []
        cost = []
        from_to = []
        n_dir = []
        content = []
        aut = []
        code = []
        n_from = []
        n_to = []
        for i in l:
            title.append(i['title'])
            url.append(i['loc'])
            times.append(time.strftime("%Y-%m",time.localtime(int(i['start_time']))))
            #times.append(time.strftime("%Y-%m",time.localtime(i[])))
            days.append(i['time'])
            try:
                if i['avg_cost'] == 1:
                    cost.append('0-500')
                elif i['avg_cost'] == 2:
                    cost.append('500-1000')
                elif i['avg_cost'] == 3:
                    cost.append('1000-3000')
                elif i['avg_cost'] == 4:
                    cost.append('3000-5000')
                elif i['avg_cost'] == 5:
                    cost.append('5000-10000')
                elif i['avg_cost'] == 6:
                    cost.append('10000-15000')
                elif i['avg_cost'] == 7:
                    cost.append('15000 +')
                else:
                    cost.append('error')
            except BaseException as e:
                print(e)
                cost.append('?')
            n_from.append(i['departure'])
            n_to.append('、'.join(i['destinations']))
            aut.append(i['nickname'])
            temp = node(i['loc'])
            write_time.append(temp.write_time)
            n_dir.append(temp.dir)
            code.append(temp.code)
            content.append(temp.content)
            print('node sleep....')
            time.sleep(10)

        return (title,url,times,days,cost,n_from,n_to,aut,write_time,n_dir,code,content)


    def write_excel(self,file_name,tup:tuple):
        title,url,times,days,cost,n_from,n_to,aut,write_time,n_dir,code,content = tup
        msg = pandas.DataFrame(data={'url':url,'标题':title,'游记时间(年度整理)':write_time,'天数':days,'时间':times,'人均费用':cost,'from':n_from,'to':n_to,'游记内容':content,'code':code,'作者':aut,'目录':n_dir})
        if os.path.exists('%s.xlsx' % file_name):
            org_msg = pandas.read_excel('%s.xlsx' % file_name)
            msg = pandas.concat([org_msg,msg],ignore_index=True)
        writer = pandas.ExcelWriter('%s.xlsx' % file_name)
        msg.to_excel(writer,'Sheet1')
        writer.save()

url = 'https://lvyou.baidu.com/notes/28d309c25c2591f008f74466'

w = list_msg()

for i in range(300,757,6):
    with open('log','w+') as f:
        f.write(str(i))
    w.write_excel('result',w.iter(w.get_list(i)))
    print('%s data has been writed...' % str(i))
    time.sleep(30)