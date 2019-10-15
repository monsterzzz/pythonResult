import datetime

a = datetime.datetime(2019,4,1,20,42,0)
b = datetime.timedelta(hours=168)
print(a + b)
print(datetime.datetime.now() + b)