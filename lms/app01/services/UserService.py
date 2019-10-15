from app01 import models
from django.forms.models import model_to_dict
from django.db import transaction
import traceback

class UserService:
    def __init__(self):
        self.obj = models.DB_user.objects
        self.bss = models.BookState.objects

    def remove_user(self,uid):
        try:
            with transaction.atomic():
                self.obj.filter(uid = uid).delete()
                self.bss.filter(uid = uid).delete()
            return True
        except:
            traceback.print_exc()
            return False

    def query_all_user(self):
        return [model_to_dict(i) for i in self.obj.all()]

    def change_power(self,uid,p):
        try:
            has_set_p = model_to_dict(self.obj.get(uid=uid))['junshi']
            if has_set_p == p:
                return "no1"
            else:
                self.obj.filter(uid=uid).update(junshi=p)
                return True
        except:
            return "no2"

    def add_user(self,name,password,address,student_id):
        if len(self.obj.filter(student_id = student_id)) > 0:
            print("!!@@#")
            return False
        else:
            self.obj.create(
                address = address,
                name = name,
                password = password,
                student_id = student_id,
            )
            return True
    
    def delete_user(self,uid):
        try:
            self.obj.filter(uid = uid).delete()
            return True
        except:
            return False

    def update_user(self,uid,password):
        try:
            self.obj.filter(uid = uid).update(password = password)
            return True
        except:
            return False

    def query_user(self,**kargs):
        if len(kargs) > 2:
            return False
        else:
            parma = []
            for i in kargs:
                if i == "name":
                    kargs[i] = "'{}'".format(kargs[i])
                    parma.append("{}__contains={}".format(i,kargs[i]))
                else:
                    parma.append("{}={}".format(i,kargs[i]))
            parma = ",".join(parma)
            result = eval("self.obj.filter({})".format(parma))
            result = [model_to_dict(i) for i in result]
            return result

    def cheak_login(self,student_id,password):
        try:
            u = self.obj.get(student_id = student_id,password = password)
            return model_to_dict(u)
        except:
            return False

    def get_all_user(self):
        pass

    def name_is_exist(self,name):
        if len(self.obj.filter(name = name)) > 0:
            return True
        else:
            return False

