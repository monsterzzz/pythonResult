"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import serve
from django.conf import settings
from app01 import views
from app01.contorller import IndexContorller,BookContorller,LendContorller,AdminContorller


urlpatterns = [
    # 管理员账户登陆
    # url(r'^admin/', admin.site.urls),
    # # 出版社列表
    # url(r'^publisher_list/', views.publisher_list),
    # url(r'^add_publisher/', views.add_publisher),
    # url(r'^drop_publisher/', views.drop_publisher),
    # url(r'^edit_publisher/', views.edit_publisher),
    # url(r'^book_list/', views.book_list),
    # url(r'^add_book/', views.add_book),
    # url(r'^drop_book/', views.drop_book),
    # url(r'^edit_book/', views.edit_book),
    # url(r'^author_list/', views.author_list),
    # url(r'^add_author/', views.add_author),
    # url(r'^drop_author/', views.drop_author),
    # url(r'^edit_author/', views.edit_author),
    # url(r'/', login.index_and_login),

    url(r'sign_in/', IndexContorller.sign_in),
    url(r"^$",IndexContorller.index_and_login),
    path("log_out/",IndexContorller.log_out),
    path("user_msg/",LendContorller.user_msg),
    url(r"book_index/",BookContorller.book_index),
    url(r"book_list/",BookContorller.book_list),
    path(r"book_detail/<int:bid>",BookContorller.book_detail),
    path("book_rest/user_query/",BookContorller.user_query),

    url(r"book_rest/add/",BookContorller.add_book),
    url(r"book_rest/all/",BookContorller.query_page_book),
    url(r"book_rest/addnum/",BookContorller.add_num),
    url(r"book_rest/subbook/",BookContorller.sub_num),
    url(r"book_rest/remove/",BookContorller.remove_book),
    url(r"book_rest/update/",BookContorller.update_book),

    url("book_rest/query/",BookContorller.query_book),
    url("lend_rest/lend/",LendContorller.lend_book),
    url("lend_rest/continue/",LendContorller.continue_lend),
    url("lend_rest/back_book/",LendContorller.back_book),
    url("lend_rest/pay_book/",LendContorller.pay_book),

    url("admin_index/",AdminContorller.admin_index),
    url("admin/book_set/",AdminContorller.book_set),
    url("admin/user_set/",AdminContorller.user_set),

    url("admin_contorl/user/change_power/",AdminContorller.change_power),
    url("admin_contorl/user/remove/",AdminContorller.remove_user),


    #url("lend_rest/index/",LendContorller.msg_query),



    url("img_upload/",BookContorller.img_upload),
    url("MEDIA/pic/(?P<path>.*)",serve,{'document_root': settings.MEDIA_ROOT + "/pic"}),





    
    #url(r'^$', views.publisher_list),
] 
