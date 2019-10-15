import requests
import hashlib
import json
import time
from bs4 import BeautifulSoup


class Crakeme:
    def __init__(self):
        self.sec_word = "c9d6618dbc657b41a66eb0af952906f1"
    
    def get_sn(self,content = None):
        data = json.dumps(content).replace(" ","") + self.sec_word
        #data = content
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()[2:12]


class Mafengwo_Spider:
    def __init__(self):
        self.worker = Crakeme()
        self.ip_port = 'transfer.mogumiao.com:9001'
        self.appKey = "TUl3d3pKT2dNNEd4ak41Nzo0dDRYMUFNN0dkeUs0Zzdz"
        self.proxies = {"http": "http://" + self.ip_port, "https": "https://" + self.ip_port}
        self.header = self.make_header()
    
    def make_header(self):
        header = {
            "Proxy-Authorization": 'Basic '+ self.appKey,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        return header
    
    def get_router(self,page):
        data = {
            "_ts":"{}".format(round(time.time() * 1000)),
            "iMddid":"10444",
            "iPage":"{}".format(page),
            "iTagId":"0",
            "sAct":"KMdd_StructWebAjax|GetPoisByTag",
        }
        data['_sn'] = self.worker.get_sn(data)
        url = "http://www.mafengwo.cn/ajax/router.php"
        r = requests.post(url,data=data,headers = self.header,proxies=self.proxies)
        r.encoding = "utf-8"
        resp = r.json()['data']
        soup = BeautifulSoup(resp['list'],'lxml')
        result = []
        li_list = soup.find_all("li")
        for li in li_list:
            tmp_dict = {}
            tmp_dict['name'] = li.find("a")['title']
            tmp_dict['href'] = "http://www.mafengwo.cn" + li.find("a")['href']
            tmp_dict['little_img'] = li.find("img")['src']
            result.append(tmp_dict)
        return result

    def get_detail(self,url):
        page_id = url.split("/")[-1].split(".")[0]
        r = requests.get(url,headers = self.header,proxies=self.proxies)
        r.encoding = "utf-8"
        resp = r.text
        result = {}
        soup = BeautifulSoup(resp,'lxml')
        try:
            photos = soup.find("a",attrs={"class":"photo"}).find_all("img")
            result['photos'] = [i['src'] for i in photos]
        except:
            result['photos'] = []
        try:
            result['desc'] = soup.find("div",attrs={"class":"summary"}).get_text(strip=True)
        except:
            result['desc'] = ""
        try:
            result['tel'] = soup.find("li",attrs={"class":"tel"}).find("div",attrs={"class":"content"}).get_text(strip=True)
        except:
            result['tel'] = ""
        try:
            result['pay_time'] = soup.find("li",attrs={"class":"item-time"}).find("div",attrs={"class":"content"}).get_text(strip=True)
        except:
            result['pay_time'] = ""
        try:
            result['jt'] = soup.find("dt",text="交通").next_sibling.next_sibling.get_text(strip=True)
        except:
            result['jt'] = ""
        try:
            result['money'] = soup.find("dt",text="门票").next_sibling.next_sibling.get_text(strip=True)
        except:
            result['money'] = ""
        try:
            result['open_time'] = soup.find("dt",text="开放时间").next_sibling.next_sibling.get_text(strip=True)
        except:
            result['open_time'] = ""

        # photos = soup.find("a",attrs={"class":"photo"}).find_all("img")
        # result['photos'] = [i['src'] for i in photos]
        # result['desc'] = soup.find("div",attrs={"class":"summary"}).get_text(strip=True)
        # result['tel'] = soup.find("li",attrs={"class":"tel"}).find("div",attrs={"class":"content"}).get_text(strip=True)
        # result['pay_time'] = soup.find("li",attrs={"class":"item-time"}).find("div",attrs={"class":"content"}).get_text(strip=True)
        # result['jt'] = soup.find("dt",text="交通").next_sibling.next_sibling.get_text(strip=True)
        # result['money'] = soup.find("dt",text="门票").next_sibling.next_sibling.get_text(strip=True)
        # result['open_time'] = soup.find("dt",text="开放时间").next_sibling.next_sibling.get_text(strip=True)
        
        
        # dl_li = soup.find("div",attrs={"class":"mod mod-detail"}).find_all("dl")
        
        # for i in dl_li:
        #     key = i.find("dt").get_text(strip=True)
        #     value = i.find("dd").get_text(strip=True)
        #     result[key] = value
        result['page_id'] = page_id
        return result

    def get_comment(self,page_id):
        page_dic = {
            "poi_id":"{}".format(page_id),"page":1,"just_comment":1
        }
        data = {
            "_ts" : "{}".format(round(time.time() * 1000)),
            "parmas" : json.dumps(page_dic)
        }
        header = {
            "Proxy-Authorization": 'Basic '+ self.appKey,
            "Referer":"http://www.mafengwo.cn/poi/{}.html".format(page_id),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        sn = self.worker.get_sn(data)
        _ts__sn = "&_ts={}&_sn={}&_={}".format(data['_ts'],sn,data['_ts'])
        url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?params=%7B%22poi_id%22%3A%22{}%22%2C%22page%22%3A{}%2C%22just_comment%22%3A{}%7D"
        url = url.format(page_dic['poi_id'],page_dic['page'],page_dic['just_comment']) + _ts__sn
        r = requests.get(url,headers=header,proxies=self.proxies)
        r.encoding="utf-8"
        resp = r.json()
        result = []
        if "暂无内容" in resp['data']['html']:
            print("#暂无内容",page_id)
            return result
        soup = BeautifulSoup(resp['data']['html'],'lxml')
        li_list = soup.find_all("li",attrs={"class":"rev-item comment-item clearfix"})
        for i in li_list:
            tmp_dic = {}
            tmp_dic['name'] = i.find("a",attrs={"class":"name"}).get_text(strip=True)
            tmp_dic['comment'] = i.find("p",attrs={"class":"rev-txt"}).get_text(strip=True)
            result.append(tmp_dic)
        return result

    def get_a_place(self,url):
        pass


s = Mafengwo_Spider()


#print(s.get_detail("http://www.mafengwo.cn/poi/3399.html"))
import random
import traceback

def worker(obj):
    s = Mafengwo_Spider()
    time.sleep(random.randint(1,2))
    try:
        print(obj['name'])
        url = obj['href']
        detali = s.get_detail(url)
        obj['detail'] = detali
        page_id = detali['page_id']
        comment = s.get_comment(page_id)
        obj['comment'] = comment
        with open("msg/{}.txt".format(obj['name']),'w+',encoding="utf-8") as f:
            f.write(str(obj))
        print("msg/{}.txt has done!".format(obj['name']))
    except Exception as e :
        traceback.print_exc()
        print("!!!!!!!!!!!!!!")
        with open("msg/error.txt",'a+',encoding="utf-8") as f:
            f.write(str(obj))
            f.write("\n")



def tt(i):
    print(i)

# from multiprocessing import Process,Pool

# if __name__ == "__main__":
#     pool = Pool(6)
#     for i in range(82):
#         print(i)
#         router = s.get_router(i+1)
#         time.sleep(2)
#         for idx in range(len(router)):
#             pool.apply_async(worker,(router[idx],))
#     pool.close()
#     pool.join()
s = Mafengwo_Spider()
for i in range(1,82):
    router = s.get_router(i+1)
    print(i)
    for i in router:
        print(i)
        try:
            url = i['href']
            detali = s.get_detail(url)
            i['detail'] = detali
            page_id = detali['page_id']
            comment = s.get_comment(page_id)
            i['comment'] = comment
            with open("msg/{}.txt".format(i['name']),'w+',encoding="utf-8") as f:
                f.write(str(i))
        except:
            traceback.print_exc()
            with open("msg/error.txt",'w+',encoding="utf-8") as f:
                f.write(str(i))

# print(s.get_router(13))
# if __name__ == "__main__":
    
#     pool = Pool(4)
#     for i in range(82):
#         router = s.get_router(i+1)
#         time.sleep(3)
#         r = requests.get("http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=994f46414a524f3fba874f2169f8b19e&count=20&expiryDate=0&format=2&newLine=2")
#         proxies = [{"http": "http://{}".format(i),"https": "http://{}".format(i)} for i in r.text.strip().split("\r\n")]
#         pool.apply_async(worker, args=(router,proxies))
#     pool.close()
#     pool.join()
#     # p = multiprocessing.Process(target = worker, args = (3,))
#     # p.start()


