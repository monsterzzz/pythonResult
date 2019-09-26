from engin import app,db
from sqlalchemy import and_
from flask import render_template,jsonify,session,request,redirect,make_response
from engin.models import *
import random


def login_requierd(func):
    def wrapper(*args, **kwargs):
        if not session.get("id"):
            return redirect("/login")
        else:
            return func(*args, **kwargs)
    return wrapper


@app.route("/",endpoint="index")
@app.route("/index",endpoint="index")
@login_requierd

def index():
    
    

    cctvList = Cctv.query.all()
    return render_template("cctv.html",cctvList=cctvList)

@app.route("/charts/<string:file>",endpoint="charts",methods=["GET","POST"])
@login_requierd
def charts(file):
    if request.method == "GET":
        return render_template("charts.html")
    option = {
        "title": {
            "text": ""
        },
        "tooltip": {},
        "legend": {
            "data": []
        },
        "xAxis": {
            "data": []
        },
        "yAxis": {},
        "series": [{
            "name": '销量',
            "type": 'bar',
            "data": []
        }],
        "warning":False

    }
    
    if file == "ph":
        minDoor = 5
        maxDoor = 7
        phs = Ph.query.all()
        option["title"]["text"] = "PH"
        option["legend"]["data"].append("值")
        option["series"][0]["name"] = "Ph"
        option["series"][0]["type"] = "line"
        option["minDoor"] = minDoor
        option["maxDoor"] = maxDoor
        for i in phs:
            option["xAxis"]["data"].append(i.time)
            option["series"][0]["data"].append(i.data)
            if float(i.data) < minDoor or float(i.data) > maxDoor:
                option["warning"] = True
        return jsonify(option)
    elif file == "bod":
        minDoor = 40
        maxDoor = 50
        bods = Bod.query.all()
        option["title"]["text"] = "Bod"
        option["legend"]["data"].append("值")
        option["series"][0]["name"] = "Bod"
        option["series"][0]["type"] = "line"
        option["minDoor"] = minDoor
        option["maxDoor"] = maxDoor
        for i in bods:
            option["xAxis"]["data"].append(i.time)
            option["series"][0]["data"].append(i.data)
            if float(i.data) < minDoor or float(i.data) > maxDoor:
                option["warning"] = True
        return jsonify(option)
    elif file == "cod":
        minDoor = 40
        maxDoor = 45
        cods = Cod.query.all()
        option["title"]["text"] = "Cod"
        option["legend"]["data"].append("值")
        option["series"][0]["name"] = "Cod"
        option["series"][0]["type"] = "line"
        option["minDoor"] = minDoor
        option["maxDoor"] = maxDoor
        for i in cods:
            option["xAxis"]["data"].append(i.time)
            option["series"][0]["data"].append(i.data)
            if float(i.data) < minDoor or float(i.data) > maxDoor:
                option["warning"] = True
        return jsonify(option)
    else:
        return jsonify(option)


@app.route("/send",endpoint="send")
@login_requierd
def send():
    admins = Rcpt.query.all()
    result = [i.toJson() for i in admins]
    return jsonify(result)

@app.route("/login",methods=["GET","POST"],endpoint="login")
def login():
    # u = User.query.all()
    # if len(u) == 0:
    #     u_item = User(name = "test",password="123")
    #     db.session.add(u_item)
    #     db.commit()

    # p = Ph.query.all()
    # if len(p) == 0:
    #     for i in range(20):
    #         p = Ph(time="1905{:0>2d}".format(i),data=round( 6 + random.random(),2 ),remark="ok")
    #         c = Cod(time="1905{:0>2d}".format(i),data=round( 40 + (random.random() * 10),2 ),remark="ok")
    #         b = Bod(time="1905{:0>2d}".format(i),data=round( random.randint(10,50) + random.random(),2 ),remark="ok")
    #         db.session.add(p)
    #         db.session.add(c)
    #         db.session.add(b)
    #     for i in range(4):
    #         r = Rcpt(name="张{}".format(i),number=str(random.randint(10000000000,99999999900)),email="{}@qq.com".format(random.randint(100000000,999999999)))
    #         db.session.add(r)
    #     db.session.commit()


    #     for i in range(24):
    #         c = Cctv(avatar = "/static/img/{}.jpg".format(random.randint(0,4)),port="{}".format(random.randint(0,100)))
    #         db.session.add(c)
    #     db.session.commit()


    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "" or password == "":
        return jsonify({
            "status" : 99999,
            "data" : "error parmar"
        })
    else:
        u = db.session.query(User).filter(and_(User.name == username,User.password == password)).all()
        if len(u) > 0:
            session['id'] = u[0].id
            return "success"
        else:
            return "false"


@app.route("/logout",endpoint="logout")
def logout():
    session.pop("id")
    return redirect("/login")