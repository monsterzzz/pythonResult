from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .myforms import sign_form
from heart_test.models import *
import uuid
import random
from django.forms.models import model_to_dict
from django.shortcuts import redirect
import json
from django.urls import reverse 
from heart_test.anser_anls import scl_90

# Create your views here.


# 首页
def index_html(request,msg=None):
    return render(request,"index.html",{"msg":msg}) # 服务器渲染

# 注册页
def sign_in(request):
    if request.method == "POST":
        forms = sign_form.SignForm(request.POST)
        if forms.is_valid():
            error_msg = ""
            account = forms.cleaned_data.get("account")
            password = forms.cleaned_data.get("password")
            try:
                User.objects.get(account=account)
                error_msg = "该账户已存在"
                return render(request,"sign_in.html",{"myform":forms,"msg":error_msg}) # 服务器渲染
            except:
                User.objects.create(account=account,password=password,uid=random.randint(1,100000))
                return render(request,"sign_in.html",{"myform":forms,"msg":"注册成功!"}) # 服务器渲染
            # database orm...
        else:
            error_msg = "输入数据不合法"
            return render(request,"sign_in.html",{"myform":forms,"msg":error_msg}) # 服务器渲染
    else:
        forms = sign_form.SignForm()  #django表单
    return render(request,"sign_in.html",{"myform":forms}) # 服务器渲染


# 登录页
# 采用ajax
# 返回json数据判断是否登录成功
def login(request):
    if request.method == "POST":
        account = request.POST.get("account")
        password = request.POST.get("password")
        status = request.POST.get("login_opt")
        print(status)
        if status == "student":
            try:
                user_msg = User.objects.get(account = int(account))
                user_msg = model_to_dict(user_msg)
                if password == user_msg['password']:      
                    result = {
                        "code" : 102,
                        "msg" : "登录成功!"
                    }        
                    response = HttpResponse(json.dumps(result))        
                    response.set_cookie("user_info",json.dumps(user_msg))
                    return response
                else:
                    result = {
                        "code" : 101,
                        "msg" : "账户名或者密码错误!"
                    }
                return HttpResponse(json.dumps(result))
            except Exception as e:
                print("e",e)
                print("!!!!!")
                result = {
                    "code" : 101,
                    "msg" : "账户名或者密码错误!"
                }
                return HttpResponse(json.dumps(result))
        elif status == "teacher":
            try:
                current_teacher = Teacher.objects.get(account=account)
                teacher_dict = model_to_dict(current_teacher)
                if teacher_dict['password'] == password:
                    code = 100
                    msg = "登录成功"
                    res = HttpResponse(json.dumps({
                        "code" : code,
                        "msg" : msg
                    }))
                    teacher_dict['is_teacher'] = True
                    res.set_cookie("user_info",json.dumps(teacher_dict))
                else:
                    code = 101
                    msg = "账户名或者密码错误"
                    res = HttpResponse(json.dumps({
                        "code" : code,
                        "msg" : msg
                    }))
                return res
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({
                    "code" : 102,
                    "msg" : "账户名或者密码错误"
                }))
    
    return HttpResponse("hello")

# 获得当前用户
# 用户信息保存在cookie中
def get_user(request):
    cookie = request.COOKIES
    user_info = json.loads(cookie['user_info'])
    return user_info

# 服务器渲染一个页面返回
# 页面使用ajax与服务器进行通信
def user_msg(request):
    user_info = get_user(request)
    return render(request,"user_msg.html",{"user":user_info})


# 补充信息 如果用户没有补充完整信息 则无法进行问卷的填写
# 在中间件中进行了对 是否补充完整信息的判断
def full_msg(request):
    form = sign_form.FullMsg()
    if request.method == "POST":
        user = get_user(request)
        uid = user['uid']
        form = sign_form.FullMsg(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            sex = form.cleaned_data.get("sex")
            age = form.cleaned_data.get("age")
            family = form.cleaned_data.get("family")
            address_type = form.cleaned_data.get("address_type")
            marry_type = form.cleaned_data.get("marry_type")
            try:
                User.objects.filter(uid=uid).update(name=name,sex=sex,age=age,family_type=family,address_type=address_type,marry_type=marry_type,is_full=1)
                update_uesr = User.objects.get(uid=uid)
                user = model_to_dict(update_uesr)
                response = redirect("../user_msg/")
                response.set_cookie("user_info",json.dumps(user))
                return response
            except Exception as e:
                print(e)
                return render(request,"full_msg.html",{"forms":form})
        else:
            return render(request,"full_msg.html",{"forms":form})
                
    else:
        return render(request,"full_msg.html",{"forms":form})

# 获取问卷列表
def question_list(request):
    return render(request,"question_list.html")

# 每次回答10个问题 避免前端页面太长
def get_ten_question(request):
    q_name = request.GET.get("q_name")
    q_index = int(request.GET.get("q_index"))
    question = Question.objects.get(q_name = q_name)
    q_dict = model_to_dict(question)
    true_index = q_index * 10
    question_list = json.loads(q_dict['q_que'])
    try:
        if q_index == 0:
            ten_question = question_list[:10]
        else:
            
            ten_question = question_list[true_index:true_index + 10]
            
        code = 200
    except Exception as e:
        code = 201
        ten_question = []
    if question_list[true_index:true_index + 11] == ten_question:
        is_end = True
    else:
        is_end = False
    result = {
        "code" : code,
        "msg" : ten_question,
        "is_end" : is_end
    }
    return HttpResponse(json.dumps(result))

# 分析数据
def answer_anls(request):
    question_name = request.GET.get("question_name")
    user = json.loads(request.COOKIES['user_info'])
    db_user = User.objects.get(iid = user['iid'])
    q = Question.objects.get(q_name = question_name)
    question_obj = Answer.objects.filter(uid = db_user,question = q)
    answer_list = []
    for i in question_obj:
        model_dict = model_to_dict(i)
        the_answer = []
        for j in json.loads(model_dict['u_ans']):
            the_answer.append(j['p_ans'])
        answer_list.append(scl_90.Scl_90(the_answer).anls())
    return render(request,"show_anls.html")

# 把数据库中的数据变为一个纯数字的列表
def get_answer_list_tool(input_string):
    score_list = []
    input_list = json.loads(input_string)
    for i in input_list:
        score_list.append(i['p_ans'])
    return score_list


# 获取每次测试的详细数据
def get_anls_item(request):
    user = json.loads(request.COOKIES['user_info'])
    aid_list = Answer.objects.filter(uid=User.objects.get(iid=user['iid'])).values("aid")
    flag = True
    for i in aid_list:
        if int(request.GET.get("aid")) == i['aid']:
            flag = False
            break
        else:
            flag = True
    
    if flag:
        return HttpResponse("false")
    else:
        current_answer = Answer.objects.get(aid=int(request.GET.get("aid")))
        answer_dict = model_to_dict(current_answer)
        result = scl_90.Scl_90(get_answer_list_tool(answer_dict['u_ans'])).anls()
        return HttpResponse(json.dumps(result))
        
# 只是渲染一个页面
# ajax通信
def anls_html(request):
    return render(request,"show_anls.html")


# 把问题答案加入数据库
def add_question_answer(request):
    if request.method == "POST":
        value_dict = json.loads(request.body)
        q_name = value_dict.get("qid")
        answer = value_dict.get("answer")
        cookie = request.COOKIES
        user_info = json.loads(cookie["user_info"])
        iid = user_info['iid']
        try:
            Answer.objects.create(question=Question.objects.get(q_name=q_name),uid=User.objects.get(iid=iid),u_ans=json.dumps(answer))
            anls_result = anls_form(answer)
            uid = User.objects.get(iid=iid)
            qid = Question.objects.get(q_name = q_name)
            test_result.objects.create(uid=uid,question=qid,body=anls_result['body'],qiangbo=anls_result['qiangpo'],renji=anls_result['renji'],yiyu=anls_result['yiyu'],jiaolv=anls_result['jiaolv'],didui=anls_result['didui'],kongbu=anls_result['kongbu'],pianzhi=anls_result['pianzhi'],all_score=anls_result['all_score'],jingshenbing=anls_result['jingshenbing'])
            result = {
                "code" : 300,
                "msg" : "添加成功！"
            }
            return HttpResponse(json.dumps(result))
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
            result = {
                "code" : 301,
                "msg" : "{}".format(e)
            }
            return HttpResponse(json.dumps(result))
    else:
        pass

def sum_tool(input_list):
    #print(input_list)
    score_list = []
    input_list = json.loads(input_list)
    for i in input_list:
        score_list.append(i['p_ans'])
    return sum(score_list)


# 注销 
# 重定向到主页并且清除cookie
def log_out(request):
    resp = redirect("/")
    resp.delete_cookie('user_info')
    return resp

# 获取最近7次问题
def get_answer_list(request):
    user = json.loads(request.COOKIES['user_info'])
    user_obj = User.objects.get(iid=user['iid'])
    answer_list = Answer.objects.filter(uid=user_obj).values("aid","question","u_ans","a_date")
    answer_type_list = []
    answer_result = []
    #print(answer_list)
    for i in answer_list:
        question_query_set = Question.objects.get(qid = i['question'])
        question_dict = model_to_dict(question_query_set)
        time_str = i['a_date'].strftime("%y/%m/%d %H:%M:%S")
        result = {
            "qid" : question_dict['qid'],
            "q_name" : question_dict['q_name'],
            "q_des" : question_dict['q_des'],
            "a_date" : time_str,
            "aid" : i["aid"],
            "all_score" : sum_tool(i['u_ans']),
            "pinjun_score" : round(sum_tool(i['u_ans'])/90,2)
        }
        answer_type_list.append(i['question'])
        answer_result.append(result)
    answer_idx = int(request.GET.get("idx"))
    answer_result = list(reversed(answer_result))
    if answer_idx == 0:
        current_seven_item = answer_result[:7]
        if current_seven_item == answer_result[:8]:
            has_next = False
        else:
            has_next = True
    else:
        current_seven_item = answer_result[ answer_idx * 7 : (answer_idx * 7) + 7]
        if current_seven_item == answer_result[ answer_idx * 7 : (answer_idx * 7) + 7 + 1]:
            has_next = False
        else:
            has_next = True
    if current_seven_item:
        code = 400
    else:
        code = 401
    result = {
        "code" : code,
        "msg" : current_seven_item,
        "has_next" : has_next
    }
    return HttpResponse(json.dumps(result))

   # return render(request,"user_msg.html",{"question_list":answer_result})


def user_msg_html(request):
    return render(request,"user_msg.html")

    #return HttpResponse("hh")

def get_test_list(request):
    with open("heart_test/scl_90.json",'r',encoding="utf-8") as f: # 打开文件
        data = f.read()  # 读取文件
    json_msg = json.loads(data)  # 把文件的字符串转换为 python 中的字典
    Question.objects.filter(qid=1).update(q_que=json.dumps(json_msg)) # 更新数据库
    # Question.objects.create(q_name = "scl_90",q_des="hello",q_que=json.dumps(json_msg))
    # question_list = Question.objects.get(q_name="scl_90")
    test_list = Question.objects.all()
    question_list = []
    for i in test_list:
        question_item = model_to_dict(i)
        question_item['sort_des'] = question_item['q_des'][:35] + "..."
        question_list.append(question_item)
    return render(request,"test_list.html",{"questions":question_list})
    #print(test_list)

def create_teacher(request):
    Teacher.objects.create(name="monster",account="qq",password="1")


# 管理员html页面
def teacher_ctrl(request):
    return render(request,"teacher_ctrl.html")


# 把答案组合为一个一个的列表 [[],[],[]] 
def get_t_data(answer_list):
    input_list = []
    for item in answer_list:
        #print(item)
        item_dict = model_to_dict(item)
        #print(item_dict,type(item_dict))
        input_list.append(get_answer_list_tool(item_dict['u_ans']))
    return input_list


# 管理员获取数据
def teacher_ctrl_data(request):
    parma = request.GET.get("parma")
    qid = Question.objects.get(q_name="scl_90")
    if parma == "all":
        answer_list = Answer.objects.filter(question=qid)
        input_list = get_t_data(answer_list)
    elif parma == "boy" or parma == "girl":
        if parma == "boy":
            sex = 1
        else:
            sex = 2
        find_list = User.objects.filter(sex=sex)
        input_list = []
        for i in find_list:
            answer_list = Answer.objects.filter(question=qid,uid=i)
            data = get_t_data(answer_list)
            input_list += data
    elif parma == "danqin" or parma == "budanqin":
        if parma == "danqin":
            flag = 1
        else:
            flag = 2
        find_list = User.objects.filter(family_type=flag)
        input_list = []
        for i in find_list:
            answer_list = Answer.objects.filter(question=qid,uid=i)
            data = get_t_data(answer_list)
            input_list += data
    elif parma == "unmarry" or parma == "marryed" or parma == "marryoff":
        if parma == "unmarry":
            flag = 1
        elif parma == "marryed" :
            flag = 2
        else:
            flag = 3
        find_list = User.objects.filter(marry_type=flag)
        input_list = []
        for i in find_list:
            answer_list = Answer.objects.filter(question=qid,uid=i)
            data = get_t_data(answer_list)
            input_list += data
    elif parma == "city" or parma == "uncity" :
        if parma == "city":
            flag = 1
        else:
            flag = 2
        find_list = User.objects.filter(address_type=flag)
        input_list = []
        for i in find_list:
            answer_list = Answer.objects.filter(question=qid,uid=i)
            data = get_t_data(answer_list)
            input_list += data
    else:
        input_list = []
    result = scl_90.Scl_90().get_health(input_list)
    return HttpResponse(json.dumps(result))

# def get_detail_item(request):
#     parma = request.GET.get("parma")
#     get_test_result_item(parma)

# def get_test_result_item(parma):
#     db_data = test_result.objects.values(parma)
#     result = {
#         "health" : [],
#         "ill" : []
#     }
#     for i in db_data:
#         if i[parma] == 1:
#             result['ill'].append()
#         else:
#             health_num += 1
#     print(db_data)

def anls_form(form_data):
    current_anser = []
    for i in form_data:
        current_anser.append(i['p_ans'])
    all_score = sum(current_anser)
    w = scl_90.Scl_90().parse_item_data(current_anser)
    w['all_score'] = all_score
    return w

