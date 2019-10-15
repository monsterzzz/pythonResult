from django.shortcuts import render,HttpResponse,redirect
from app01.services import LendService
import json


def user_msg(request):
    user = request.session.get("user")
    uid = user['uid']
    result = LendService.LendService().query_lend(uid)
    return render(request,"user_msg.html",{"down":result[0],"not_down":result[1]})


def lend_book(request):
    bid = json.loads(request.body)['bid']
    uid = request.session['user']['uid']
    service = LendService.LendService()
    result = service.lend_book(int(bid),uid)
    if result:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")

def back_book(request):
    bsid = request.GET.get("bsid")
    uid = request.session['user']['uid']
    service = LendService.LendService()
    flag = service.back_book(bsid,uid)
    if flag:
        return HttpResponse(json.dumps(flag))
    else:
        return HttpResponse("no")

def pay_book(request):
    bsid = request.GET.get("bsid")
    uid = request.session['user']['uid']
    service = LendService.LendService()
    flag = service.pay_book(bsid,uid)
    if flag:
        return HttpResponse(json.dumps(flag))
    else:
        return HttpResponse("no")

def continue_lend(request):
    bsid = request.GET.get("bsid")
    uid = request.session['user']['uid']
    service = LendService.LendService()
    flag = service.continue_lend(bsid,uid)
    if flag:
        return HttpResponse(flag)
    else:
        return HttpResponse("no")


