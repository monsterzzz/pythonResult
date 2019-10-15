"""scl_90 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from heart_test import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index_html,name="index"),
    path("sign_in/",views.sign_in),
    path("login/",views.login,),
    path("user_msg/",views.user_msg),
    path("full_msg/",views.full_msg),
    path("question_list/",views.question_list),
    path("get_ten_question/",views.get_ten_question),
    path("add_answer/",views.add_question_answer),
    path("show_anls/",views.anls_html),
    path("answer_list/",views.user_msg_html),
    path("get_anls_item/",views.get_anls_item),
    path("get_seven_answer/",views.get_answer_list),
    path("test_list/",views.get_test_list),
   # path("test/",views.create_teacher),
    path("log_out/",views.log_out),
    path("teacher_ctrl/",views.teacher_ctrl),
    path("teacher_ctrl_data/",views.teacher_ctrl_data),
   # path("get_detail_data/",views.get_detail_item),




]
