import pandas
from collections import Counter

def concat_excel_tree(data_path,result_path):
    data = pandas.DataFrame()
    for i in range(1,4):
        print(data_path % str(i))
        msg = pandas.read_excel(data_path % str(i))
        content = msg
        data = pandas.concat([data,content],ignore_index=True)
    writer = pandas.ExcelWriter(result_path)
    data.to_excel(writer,'sheet1')
    writer.save()

def concat_excel_line(data_list:list,result_path:str):
    data = pandas.DataFrame()
    for i in data_list:
        data = pandas.concat([data,i],axis=1)
    writer = pandas.ExcelWriter(result_path)
    data.to_excel(writer,'sheet1')
    writer.save()

def clear_space(data):
    def c(x):
        if x == "None" or x == "none" :
            return "游记内容为空！"
        elif x == " " or x == "" or str(x) == 'nan':
            return "分词内容为空！"
        else:
            return x
    return list(map(c,data))

def write_excel(data,result_path,name ='None',is_remake = True):
    if is_remake:
        data = pandas.DataFrame(data={name:data})
    else:
        data = pandas.DataFrame(data=data)
    writer = pandas.ExcelWriter(result_path)
    data.to_excel(writer,'sheet1')
    writer.save()

def get_read_me(pdframe,read_me_name):
   # msg = pandas.read_excel('result.xlsx')
    msg = pdframe
    word = msg['分词']
    content = msg['游记内容']
    for i in range(len(content)):
        with open(read_me_name,'a+',encoding='utf-8') as f:
            try:
                if word[i].count('/') <= 50  and "！" not in content[i] and "None" not in content[i]:
                    if len(content[i]) != 0 :
                        f.write("%s : word_num : %s sp_word_num : %s \n" % (str(i),str(len(content[i])),str(word[i].count('/')+1)))
                    else:
                        f.write("%s : word_num : %s sp_word_num : %s \n" % (str(i),str(len(content[i])),str(word[i].count('/'))))
            except:
                try:
                    f.write("%s : word_num : %s \n" % (str(i),str(len(content[i]))))
                except TypeError:
                    f.write("%s : word_num : %s \n" % (str(i),str(0)))


def get_max_num(word_list:list,default_max_door = 300,):
    word =  list(map(lambda x : str(x),word_list))
    p = '/'.join(word)
    pass_word = ['几天','适合','想要','心情','下次','正好','告诉','记得','出口','反正','cn','希望','时间',"简单","样子",'可惜','方式','离开','打算','每次','事情', '乱打', '之旅',]
    for i in pass_word:
        p = p.replace(i,'')
    p = list(map(lambda x : str(x),p.split('/')))
    #print(p[1373])
    return Counter(p).most_common(default_max_door)[1:]

# d = pandas.read_excel('m_result/no_space_result.xlsx')
# get_read_me(d,'m_result/m_read_me.txt')

data = pandas.read_excel('m_result/no_space_word.xlsx')

w = data['分词']

l = get_max_num(w)

word = []
count = []
for i in l:
    word.append(i[0])
    count.append(i[1])
dic = {
    "word" : word,
    "count" : count
}

# a = pandas.read_excel('m_result/result.xlsx')
# b = pandas.read_excel('m_result/no_space_word.xlsx')
# concat_excel_line([a,b],"m_result/no_space_result.xlsx")
write_excel(dic,result_path="m_result/max_word_count1.xlsx",is_remake=False)

# data = pandas.read_excel('result.xlsx')
# word = data['分词']
# word = clear_space(word)
# write_excel(word,'m_result/no_space_word.xlsx','分词')


# msg = pandas.read_excel('c_result/all_end5.xlsx')
# get_read_me(msg,'c_result/c_read_me.txt')
# a = pandas.read_excel('c_result/d.xlsx')
# b = pandas.read_excel('c_result/no_space_result_d1.xlsx')

# concat_excel_line([a,b],"c_result/all_end5.xlsx")

# a = pandas.read_excel('c_result/end.xlsx')
# data = a['分词']
# data = clear_space(data)
# write_excel(data,"分词","c_result/no_space_result_d1.xlsx")

            #print("!!!!! %s" % str(i))

# string = "sss/sss"

# print(string.count("/"))

# string = "崇高\n"

# print(len(string))

# all_data = pandas.DataFrame()

# for i in range(1,4):
#     data = pandas.read_excel('ctr%s.xlsx' % str(i))
#     print(len(data['分词']))
#     #word = data['分词']
#     all_data = pandas.concat([all_data,data],ignore_index=True)
# #print(len(result['分词']))
# writer = pandas.ExcelWriter('ctr_result.xlsx')
# all_data.to_excel(writer,'sheet1')
# writer.save()





