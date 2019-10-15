from django.shortcuts import redirect, render, HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.core.files.storage import default_storage
from app01.services import BookService
from lms import settings
import uuid
import json


def book_index(request):
    return book_list(request)


def book_list(request):
    bs = BookService.BookService()
    btype = request.GET.get("type")
    page = request.GET.get("page")
    if not page:
        page = 1
    type_list = bs.all_type()
    if not btype or btype == "0":
        for i in type_list:
            i['is_act'] = False
        type_list = [{
            "tid" : 0,
            "name" : "所有",
            'is_act' : True
        }] + type_list
        book_data = bs.all_book()
    else:
        for i in type_list:
            if i['tid'] == int(btype):
                i['is_act'] = True
            else:
                i['is_act'] = False
        type_list = [{
            "tid" : 0,
            "name" : "所有",
            'is_act' : False
        }] + type_list
        book_data = bs.query_type_book(int(btype))
    paginator = Paginator(book_data,10)
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
    return render(request,"book_list.html",{"head":["isbn_id","书名","作者","出版社"],"books":books,"type":type_list})


def query_page_book(request):
    bookService = BookService.BookService()
    page_num = request.GET.get("page")
    if page_num:
        start = int(page_num) * 10
    else:
        start = 0
    page_book = bookService.query_all(start, start + 10)
    return HttpResponse(json.dumps(page_book))


def book_detail(request,bid):
    book = BookService.BookService().query_book_by_id(bid)
    
    return render(request, "book_detail.html", {"book": book[0]})


def user_query(request):
    type_name = request.GET.get("type_name")
    word = request.GET.get("word")
    service = BookService.BookService()
    if type_name == "name":
        result = service.query_book_by_name(word)
    elif type_name == "auth":
        result = service.query_book_by_auth(word)
    elif type_name == "bid":
        result = service.query_book_by_id(word)
    elif type_name == "pub":
        result = service.query_book_by_pub(word)
    elif type_name == "type":
        result = service.query_type_book(word)
    else:
        return HttpResponse(status=403)
    if not result:
        return HttpResponse(status=400)
    # return_key = ['bid','isbn_id','name','auther','publisher']
    # result_dict = []
    # for i in result:
    #     for j in i.keys():
    #         if j not in return_key:
    #             del i[j]
    return HttpResponse(json.dumps(result))


def query_book(request):
    type_name = request.GET.get("type_name")
    print(type_name)
    word = request.GET.get("word")
    service = BookService.BookService()
    if type_name == "name":
        result = service.query_book_by_name(word)
    elif type_name == "auth":
        print("!!!!")
        result = service.query_book_by_auth(word)
    elif type_name == "bid":
        result = service.query_book_by_id(word)
    elif type_name == "pub":
        result = service.query_book_by_pub(word)
    elif type_name == "type":
        result = service.query_type_book(word)
    else:
        return HttpResponse(status=403)
    if not result:
        return HttpResponse(status=400)
    html_str = '''
    <tr id="tr_{bid}">
        <th scope="row"> {i}</th>
        <td>{isbn_id}</td>
        <td>{name}</td>
        <td>{auther}</td>
        <td>{publisher}</td>
        <td id="book_num_{bid}">{number}</td>
        <td id="can_lend_{bid}">{can_lend}</td>
        <td>
            <button class="btn btn-default btn-sm" id="addnum" type="button" onclick="addnum({bid})">
                <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
            </button>
            <button class="btn btn-default btn-sm" id="" type="button" data-toggle="modal"
                data-target="#edit_book_{bid}">
                <span class="glyphicon glyphicon-edit" aria-hidden="true"></span>
            </button>
            <div class="modal fade bs-example-modal-lg" id="edit_book_{bid}" tabindex="-1"
                role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal"
                                aria-hidden="true">
                                &times;
                            </button>
                            <h4 class="modal-title" id="myModalLabel">
                                编辑图书
                            </h4>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-sm-3 col-sm-offset-2">
                                    <a href="#" class="thumbnail">
                                        <img src="{img_path}" id="up_{bid}" alt="...">
                                    </a>
                                </div>
                                <div class="col-sm-6">
                                    <form class="form-horizontal" style="padding-top:23%"
                                        id="img_form_{bid}" role="form">
                                        <div class="form-group bottom">
                                            <input type="file" name="img" onchange="UpdateUpLoad({bid})">
                                        </div>
                                    </form>
                                </div>
                            </div>

                            <form class="form-horizontal" id="book_msg_{bid}" role="form">
                                <div class="form-group" style="display:none;">
                                    <label for="uname" class="col-sm-2 control-label">bid</label>
                                    <div class="col-sm-9">
                                        <input type="text"  name="bid" class="form-control well" value="{bid}"
                                            />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="uname" class="col-sm-2 control-label">图书名称</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="name" name="name" class="form-control well"
                                            value="{name}" placeholder="请输入图书名称" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="upwd" class="col-sm-2 control-label">isbn_id</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="isbn_id" name="isbn_id"
                                            value="{isbn_id}" class="form-control well"
                                            placeholder="请输入isbn_id" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="upwd" class="col-sm-2 control-label">作者</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="auther" name="auther" class="form-control well"
                                            value="{auther}" placeholder="请输入作者" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="upwd" class="col-sm-2 control-label">出版社</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="publisher" name="publisher"
                                            value="{publisher}" class="form-control well"
                                            placeholder="请输入出版社" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="upwd" class="col-sm-2 control-label">价格</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="price" name="price" class="form-control well"
                                            value="{price}" placeholder="请输入价格" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="upwd" class="col-sm-2 control-label">类型</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="b_type" name="b_type" class="form-control well"
                                            value="{b_type}" placeholder="请输入类型" />
                                    </div>
                                </div>
                                <div class="form-group" style="display:none">
                                    <label for="upwd" class="col-sm-2 control-label">img_path</label>
                                    <div class="col-sm-9">
                                        <input type="text" id="img_path_{bid}" name="img_path"
                                            class="form-control well" value="{img_path}"
                                            placeholder="请输入img_path" />
                                    </div>
                                </div>
                            </form>
                            <div class="col-sm-12" id="msg_show">

                            </div>

                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">关闭
                            </button>
                            <button type="button" id="add_btn" class="btn btn-primary"
                                onclick="UpdateBook({bid},{isbn_id})">
                                提交更改
                            </button>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal -->
            </div>
            <button class="btn btn-default btn-sm" id="subbook" type="button" onclick="subBook({bid})">
                <span class="glyphicon glyphicon-minus" aria-hidden="true"></span>
            </button>
            <button class="btn btn-default btn-sm" id="removebook" type="button" onclick="removeBook({bid})">
                <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
            </button>
        </td>
    </tr>
    '''
    result_str = ""
    for i in range(len(result)):
        print(result[i]['isbn_id'])
        result_str += html_str.format(
            bid= result[i]['bid'],
            i = i + 1,
            name = result[i]['name'],
            number = result[i]['number'],
            isbn_id= result[i]['isbn_id'],
            can_lend= result[i]['can_lend'],

            b_type= result[i]['b_type'],
            img_path = result[i]['img_path'],
            auther = result[i]['auther'],
            publisher = result[i]['publisher'],
            price = result[i]['price'],
            )
    return HttpResponse(result_str)


def img_upload(request):
    img = request.FILES.get("img")
    name = uuid.uuid4()
    ret_name = "/MEDIA/pic/{}.jpg".format(name)
    file_name = "{}/pic/{}.jpg".format(settings.MEDIA_ROOT, name)
    with default_storage.open(file_name, "wb+") as f:
        for chunk in img.chunks():
            f.write(chunk)
    return HttpResponse(ret_name)


def remove_book(request):
    bid = int(request.GET.get("bid"))
    bs = BookService.BookService()
    flag = bs.remove_book(bid)
    if flag:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def add_book(request):
    name = request.POST.get("name")
    isbn_id = int(request.POST.get("isbn_id"))
    b_type = request.POST.get("b_type")
    img_path = request.POST.get("img_path")
    publisher = request.POST.get("publisher")
    auther = request.POST.get("auther")
    price = float(request.POST.get("price"))
    descri = request.POST.get("descri")
    flag = add_book_base(name, isbn_id, b_type, img_path,
                         publisher, auther, price,descri)
    if flag:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def add_num(request):
    bid = request.GET.get("bid")
    bid = int(bid)
    flag = BookService.BookService().add_book_num(bid)
    if flag:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def sub_num(request):
    bid = request.GET.get("bid")
    lend_id = request.GET.get("lend_id")
    bid = int(bid)
    if lend_id:
        flag = BookService.BookService().sub_book(bid, lend_id)
    else:
        print("!")
        flag = BookService.BookService().sub_book(bid)
    if flag == False:
        return HttpResponse("no")
    else:
        if flag == "id":
            return HttpResponse("id")
        else:
            return HttpResponse("yes")


def update_book(request):
    bs = BookService.BookService()
    bid = int(request.POST.get("bid"))
    name = request.POST.get("name")
    isbn_id = int(request.POST.get("isbn_id"))
    b_type = request.POST.get("b_type")
    img_path = request.POST.get("img_path")
    publisher = request.POST.get("publisher")
    auther = request.POST.get("auther")
    price = float(request.POST.get("price"))
    result = bs.update_book_msg(
        bid=bid,
        name=name,
        isbn_id=isbn_id,
        b_type=b_type,
        img_path=img_path,
        publisher=publisher,
        auther=auther,
        price=price
    )
    if result:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def add_book_base(name, isbn_id, b_type, img_path, publisher, auther, price,descri):
    bookService = BookService.BookService()
    flag = bookService.add_book(
        isbn_id=isbn_id,
        b_type=b_type,
        img_path=img_path,
        name=name,
        publisher=publisher,
        auther=auther,
        price=price,
        descri=descri
    )
    return flag
