import json

# a = '{"data": [{"state": "100", "name": "dd", "uid": 34557, "in_where": 321, "addr": ["127.0.0.1", 4961]}], "header": "USERLIST"}'
# json.loads(a)

a = {
    "1" : 2
}

b = a

b['1'] += 1

print(a['1'])

c = [1,2]
c[0],c[1] = c[1],c[0]
print(c)


a = "{'data': 'all', 'header': 'GET'}{'data': 'all', 'header': 'GET'}".replace("}{","}######{")

for i in a.split("######"):
    print(i)