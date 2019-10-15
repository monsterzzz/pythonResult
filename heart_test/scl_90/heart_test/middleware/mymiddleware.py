from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect
from django.http import HttpResponse
import json


## 权限管理
class MyMiddleware(MiddlewareMixin):
    def process_request(self,request):
        cookies = request.COOKIES
        if "user_info" in cookies:  #  如果已经登录成功 cookie中就会存在 user_info
            #print(cookies['user_info'])
            user_cookie = json.loads(cookies['user_info'])
            if "log_out" in request.path:  # 如果要退出 就可以退
                return None
            if "is_teacher" in user_cookie: # 如果是teacher
                if "teacher_ctrl" in request.path: # 并且访问的是管理员页面
                    return None
                else: #如果不是管理员页面就强制跳转到管理员页面
                    resp = redirect("/teacher_ctrl/")
                    return resp
            if user_cookie['is_full'] == 0: #如果是学生 并且没有完善资料
                if "full_msg" in request.path and request.GET.get("writing") : # 如果正要完善资料
                    return None
                else:  # 如果没有准备要完善 就强制跳转到完善资料页面
                    response = redirect("/full_msg?writing=1") 
                    return response
            else:
                return None
        else:  # 如果没有登录
            can_pass_url = ["/","/login/","/sign_in/"]
            if request.path in can_pass_url: 
                return None
            else: 
                return redirect("/")

    