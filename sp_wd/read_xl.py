# with open("jb_append/DIY_word.txt",'r',encoding='utf-8') as f:
#     data = f.read()
# temp = []
# for i in data.split('\n'):
#     if "(" in i:
#         temp.append(i.split("(")[0])
#     elif "（" in i:
#         temp.append(i.split("（")[0])
#     elif " " in i:
#         temp.append(i)
# with open('mm.txt','w+',encoding='utf-8') as f:
#     f.write('\n'.join(list(set(temp))))
# #print(data.split())
# with open('mm.txt','r+',encoding='utf-8') as f:
#     d = f.read()

# string1 = []
# string2 = []

# for i in d.split('\n'):
#     if " " not in i:
#         string1.append(i)
#     else:
#         string2.append(i)

# with open('mm1.txt','w+',encoding='utf-8') as f:
#     f.write('\n'.join(string1))

# with open('mm2.txt','w+',encoding='utf-8') as f:
#     f.write('\n'.join(string2))

string = "                                                                                "
with open("jb_append/stop.txt",'r',encoding='utf-8') as f:
    data = f.read()

print(string in data)