import json
import pymysql,os
 
# 打开数据库连接
db = pymysql.connect("localhost","root","123456","qingdao" )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute()  方法执行 SQL 查询 

 
# 使用 fetchone() 方法获取单条数据.

li_dir = os.listdir("msg")
for i in li_dir:
    print(i)
    if "err" in i:
        continue
    with open('{}/{}'.format("msg",i),'r',encoding="utf-8") as f:
        a = f.read()
    a = eval(a)
    #print(a['comment'])
    print(a['detail']['page_id'])

    for i in a['comment']:
        sql = '''INSERT INTO comments VALUES (NULL,{},"{}","{}")'''.format(int(a['detail']['page_id']),i['name'],i['comment'])
        try:
            cursor.execute(sql)
        except:
            pass
    db.commit()
# 关闭数据库连接

db.close()