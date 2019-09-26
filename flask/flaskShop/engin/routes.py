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
    print(session.get("id"))
    goodList = Good.query.all()
    return render_template("goodlist.html",goodList = goodList)


@app.route("/login",methods=["GET","POST"],endpoint="login")
def login():
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

@app.route("/signIn",methods=["GET","POST"],endpoint="signIn")
def signIn():
    if request.method == "GET":
        return render_template("signIn.html")
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "" or password == "":
        return jsonify({
            "status" : 99999,
            "data" : "error parmar"
        })
    else:
        u = User(name = username,password = password)
        db.session.add(u)
        db.session.commit()
        return "success"

@app.route("/cart/add/<int:gid>",methods=["GET","POST"],endpoint="cartAdd")
@login_requierd
def cartAdd(gid):
    uid = session.get("id")
    u = db.session.query(User).filter(User.id==int(uid)).first()
    g = db.session.query(Good).filter(Good.id==int(gid)).first()
    c = Cart(user=u,good=g)
    db.session.add(c)
    db.session.commit()
    return "success"


@app.route("/logout")
@login_requierd
def logOut():
    session.pop("id",None)
    return redirect("/login")


@app.route("/cart",endpoint="cart")
@login_requierd
def cart():
    # for i in range(30):
    #     g = Good(
    #         name = "商品_{}".format(i),
    #         avatar = "/static/img/{}.jpg".format(random.randint(0,8)),
    #         description = "这是商品_{}_的描述".format(i),
    #         price = random.randint(1,99)
    #     )
    #     db.session.add(g)
    # db.session.commit()
    uid = session.get("id")
    u = db.session.query(User).filter(User.id == uid).first()
    carts = u.cart
    total = 0
    goods = []
    for i in carts:
        i = i.good
        goods.append(i)
        total += i.price
    return render_template("cart.html",goods = { "total":total,"data" : goods })


@app.route("/order",endpoint="order")
@login_requierd
def order():
    uid = session.get("id")
    u = db.session.query(User).filter(User.id == int(uid)).first()
    u.cart = []
    db.session.add(u)
    db.session.commit()
    return "success"