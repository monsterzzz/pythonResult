from django.db import models
from datetime import datetime

# Create your models here.


class DB_user(models.Model):
    uid = models.AutoField(primary_key=True)
    lend_num = models.IntegerField(default=3)
    address = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    student_id = models.IntegerField()
    lend_num = models.IntegerField(default=3)
    junshi = models.IntegerField(default=0)

class UserToBook(models.Model):
    ubid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    bid = models.IntegerField()
    bsid = models.IntegerField()
    # down = models.IntegerField()
    # lend_time = models.DateTimeField(auto_created=True)
    # back_time = models.DateTimeField()

class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    isbn_id = models.IntegerField()
    b_type = models.CharField(max_length = 64)
    img_path = models.TextField(max_length=3000)
    name = models.CharField(max_length=64)
    publisher = models.TextField(max_length=1000)
    auther = models.TextField(max_length=1000)
    price = models.FloatField()
    number = models.IntegerField(default=2)
    can_lend = models.IntegerField(default=2)
    descri = models.CharField(max_length = 3000,default="暂无")
    

class BookState(models.Model):
    bsid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    lend_time = models.DateTimeField(auto_now_add=True)
    should_back_time = models.IntegerField(default=168)
    back_time = models.DateTimeField(null=True)
    down = models.IntegerField(0)
    beizhu = models.CharField(max_length = 3000,default="")



class Power(models.Model):
    pid = models.AutoField(primary_key=True)
    can_lend = models.IntegerField()
    add_user = models.IntegerField()
    delete_self = models.IntegerField()
    delete_user = models.IntegerField()
    add_book = models.IntegerField()
    delete_book = models.IntegerField()
    update_book = models.IntegerField()
    query_book = models.IntegerField()
    
class BookType(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

class TypeToBook(models.Model):
    btid = models.AutoField(primary_key=True)
    bid = models.IntegerField()
    tid = models.IntegerField()

    
class BookAdmin(models.Model):
    baid = models.AutoField(primary_key=True)
    account = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    
    
