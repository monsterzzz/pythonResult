from django.shortcuts import redirect,render,redirect,HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from app01.services import BookService,UserService

def admin_index(request):
    return render(request,"admin.html")

def change_power(request):
    power = request.GET.get("p")
    uid = request.GET.get("uid")
    if power not in ["1","0"]:
        return HttpResponse(status=400)
    else:
        us = UserService.UserService()
        result = us.change_power(int(uid),int(power))
        if result == True:
            return HttpResponse("yes")
        else:
            return HttpResponse(result)

def remove_user(request):
    uid = request.GET.get("uid")
    if not uid or not uid.isdigit():
        return HttpResponse(status=400)
    us = UserService.UserService()
    flag = us.remove_user(int(uid))
    if flag:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")

def user_set(request):
    us = UserService.UserService()
    by_type = request.GET.get("user_type")
    word = request.GET.get("word")
    page = request.GET.get("page")
    if not by_type:
        result = us.query_all_user()
    else:
        if by_type == "uid":
            result = us.query_user(uid=int(word))
        elif by_type == "name":
            result = us.query_user(name=word)
        elif by_type == "student_id":
            result = us.query_user(student_id=word)
        elif by_type == "card_id":
            result = us.query_user(card_id=word)
        else:
            return HttpResponse(status=400)
    paginator = Paginator(result,10)
    try:
        users = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        users = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        users = paginator.page(paginator.num_pages)
    resp_dict = {
        "result":users,
        "head" : ['uid',"姓名","学号","卡号","地址","可否借阅军事书籍"]
    }
    return render(request,"user_set.html",resp_dict)

def book_set(request):
    bs = BookService.BookService()
    page = request.GET.get("page")
    current_book_type = request.GET.get("book_type")
    type_list = bs.all_type()
    if not current_book_type or current_book_type == "0":
        paginator = Paginator(bs.all_book(),10)
        all_the_dict = [{
            "tid" : 0,
            "name" : "所有",
            "is_act" :True
        }]
        for i in type_list:
            i['is_act'] = False
        type_list = all_the_dict + type_list
    else:
        paginator = Paginator(bs.query_type_book(int(current_book_type)),10)
        all_the_dict = [{
            "tid" : 0,
            "name" : "所有",
            "is_act" : False
        }]
        for i in type_list:
            if i['tid'] == int(current_book_type):
                i['is_act'] = True
            else:
                i['is_act'] = False
        type_list = all_the_dict + type_list
    
    try:
        books = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        books = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        books = paginator.page(paginator.num_pages)
    return render(request,"book_set.html",{"head":["isbn_id","书名","作者","出版社","存量","可借","选项"],"books":books,"type":type_list})

