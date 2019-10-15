#import urllib.parse.quote as quote

from urllib.parse import quote,urlencode

s = {
    'word': '韩国旅游'
}
d = 'http://index.baidu.com/?tpl=trend&word=韩国旅游'
#d = '韩国旅游'
print(urlencode(s))
#print(d.decode('gb2312'))
print(d.encode('gb2312').decode('utf-8'))

 