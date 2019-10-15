from django.shortcuts import render, redirect,HttpResponse
from app01 import models
from app01.services import UserService
import traceback
import random
from django.forms import model_to_dict

def index_and_login(request):
    if request.method == "GET":
        return render(request,"index.html")
    else:
        userService = UserService.UserService()
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")
        opt = request.POST.get("login_opt")
        if opt == "student":
            user = userService.cheak_login(student_id=student_id,password=password)
            if user:
                user['is_admin'] = False
                request.session['user'] = user
                return HttpResponse("true")
            else:
                return HttpResponse("error")
        else:
            user = model_to_dict(models.BookAdmin.objects.get(account=student_id,password=password))
            if user:
                user['is_admin'] = True
                request.session['user'] = user
                return HttpResponse("admin")
            else:
                return HttpResponse("error")

def sign_in(request):
    userService = UserService.UserService();
    name = request.POST.get("name")
    password = request.POST.get("password")
    address = request.POST.get("address")
    student_id = request.POST.get("student_id")
    if not student_id.isdigit():
        return HttpResponse("no1")
    flag = userService.add_user(name=name,password=password,address=address,student_id = int(student_id))
    if not flag:
        return HttpResponse("no2")
    else:
        return HttpResponse("yes")

def log_out(request):
    s = request.session
    del s['user']
    return redirect("/")


