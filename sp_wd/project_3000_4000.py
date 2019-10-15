import jieba
from collections import Counter
from wordcloud import WordCloud
import pandas
import re,os

data = pandas.read_excel('result.xlsx')
content = data['游记内容']

class sp_wd:
    def __init__(self,word_num = 100 ):
        jieba.re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\- ]+)", re.U)
        self.user_add_dic_path = 'jb_append/DIY_word.txt'
        self.user_stop_dic_parh = 'jb_append/stop.txt'
        self.word_num = word_num
        self.cut_result = ''
        self.path = 'data/9.txt'
        self.load_DIY_word()

    def add_word_to_add_dic(self,word):
        if " " in word:
            jieba.add_word(word)
            with open('mm.txt','w+',encoding='utf-8') as f:
                f.write(word+'\n')
            print('%s has been append add dic...' % word)
        else:
            try:
                with open(self.user_stop_dic_parh,'a+',encoding='utf-8') as f:
                    f.write(str(word) + '\n')
                print('%s has been append add dic...' % word)
            except BaseException as e:
                print(e)
                print('ADD ADD WORD ERROR!')
    
    def add_word_to_stop_dic(self,word):
        try:
            with open(self.user_stop_dic_parh,'a+',encoding='utf-8') as f:
                f.write(str(word) + '\n')
            print('%s has been append to stop dic...' % word)
        except BaseException as e:
            print(e)
            print('ADD STOP WORD ERROR!')

    def load_stop_word(self):
        result = []
        if self.add_word_to_stop_dic:
            with open(self.user_stop_dic_parh,'r',encoding='utf-8') as f:
                stop_word = f.readlines()
                result = []
                for i in stop_word:
                    result.append(i.strip())
        return result

    def load_DIY_word(self):
        if self.user_add_dic_path:
            with open("jb_append/space_in_word.txt",'r',encoding='utf-8') as f:
                d = f.read()
            for i in d.split('\n'):
                jieba.add_word(i)
            jieba.load_userdict(self.user_add_dic_path)
            print('uesr add dic has been load')


    def load_wait_file(self,):
        with open(self.path,'r',encoding='utf-8') as f:
            string = f.read()
        return string

    def cut_word(self, data = '' ,level = True ,mode = True, org_msg = False):
        s = jieba.cut(data ,cut_all=level,HMM=mode)
        x = []
        for i in s:
            if i not in self.load_stop_word():
                x.append(i)
        l = [ x for x in x if len(x) >= 2 and "  " not in x and " -" not in x and ". " not in x and "--" not in x and ".." not in x and "- " not in x and x.isdigit() is not True and x.replace(".","").isdigit() is not True]
        self.cut_result = l
        return l
        
    def get_max_word(self,seq):
        result = Counter(seq).most_common(self.word_num)
        return result
    
    def make_WordCloud(self):
        my_wordcloud = WordCloud(width=1000,height=600,min_font_size=20,max_words=200,max_font_size=80,font_path="C:\WINDOWS\Fonts\simhei.ttf").generate(' '.join(w.cut_result))
        my_wordcloud.to_file('test.png')

w = sp_wd(100)
for i in range(3000,4000):
    d = []
    try:
        print(data['标题'][i])
    except:
        print('title code error!')
    #print(content[i])
    if str(content[i]) == 'nan':
        d.append('游记内容为空！')
        print("%s : nan" % str(i))
    else:
        x = w.get_max_word(w.cut_word(data=content[i],level=False))
        s = list(x)
        for k in s:
            d.append(k[0])
    print(i)
    file_name = "sss4000.xlsx"
    msg = pandas.DataFrame(data={"分词":['/'.join(d)]})
    if os.path.exists(file_name):
        org_msg = pandas.read_excel(file_name)
        msg = pandas.concat([org_msg,msg],ignore_index=True)
    writer = pandas.ExcelWriter(file_name)
    msg.to_excel(writer,'Sheet1')
    writer.save()
    # df = pandas.DataFrame(data={"分词":d})
    # writer = pandas.ExcelWriter()
    # df.to_excel(writer,index=False)
    # writer.save()
    # with open('result1.txt','a+',encoding='utf-8') as f:
    #     f.write('/'.join(d) + '\n')
    #w.path = 'data/%s.txt' % str( i+3 )
    #print('*****************************************************************************')
#w.make_WordCloud()



