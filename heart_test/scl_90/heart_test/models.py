from django.db import models

# Create your models here.

class Teacher(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class User(models.Model):
    iid = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    sex = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    family_type = models.IntegerField(default=0)
    address_type = models.IntegerField(default=0)
    marry_type = models.IntegerField(default=0)
    is_full = models.IntegerField(default=0)

    def __str__(self):
        return super().__str__() + " account: " + self.account

class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    
    q_name = models.CharField(max_length=80)
    q_des = models.CharField(max_length=400)
    q_que = models.TextField(max_length=2000)
    

class Answer(models.Model):
    aid = models.AutoField(primary_key=True)
    question = models.ForeignKey(to = Question,on_delete=models.CASCADE)
    uid = models.ForeignKey(to = User,on_delete=models.CASCADE)
    u_ans = models.TextField(max_length=2000) 
    a_date = models.DateTimeField(auto_now_add=True)


class test_result(models.Model):
    tid = models.AutoField(primary_key=True)
    question = models.ForeignKey(to=Question,on_delete=models.CASCADE)
    uid = models.ForeignKey(to=User,on_delete=models.CASCADE)
    body = models.IntegerField(default=0)
    qiangbo = models.IntegerField(default=0)
    renji = models.IntegerField(default=0)
    yiyu = models.IntegerField(default=0)
    jiaolv = models.IntegerField(default=0)
    didui = models.IntegerField(default=0)
    kongbu = models.IntegerField(default=0)
    pianzhi = models.IntegerField(default=0)
    jingshenbing = models.IntegerField(default=0)
    all_score = models.IntegerField(default=0)
