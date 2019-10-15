import jieba
from collections import Counter

file_name = 'jb_append/DIY_word.txt'
jieba.load_userdict(file_name)

with open('data/1.txt','r',encoding='utf-8') as f:
    s = f.read()

with open('jb_append/stop.txt','r',encoding='utf-8') as f:
    stop_word = f.readlines()
    res = []
    for i in stop_word:
        res.append(i.strip())
    #res = dict(res)


se = jieba.cut(s, cut_all=True, HMM=True)
with open('default.txt','w+',encoding='utf-8') as f:
    f.write("/ ".join(se))



x = []
for i in se:
    #print(i)
    if i not in res:
        x.append(i)
    
l = [ x for x in x if len(x)>=2]
c = Counter(l).most_common(100)




with open('www2.txt','w+',encoding='utf-8') as f:
    f.write(str(list(c)))

with open('ww2w1.txt','w+',encoding='utf-8') as f:
    f.write(str(res))