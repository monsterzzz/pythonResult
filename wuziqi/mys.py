import socket
import threading
import os
import time
import random
import json

class User:
    def __init__(self,name,uid,state,place):
        self.name = name
        self.uid = uid
        self.state = state
        self.place = place

class Servers:
    def __init__(self):
        self.localIP = '127.0.0.1'
        self.serverPort = 5000
        #self.corners = ()
        self.corners = []
        self.udpServer = [] # corner socket
        self.userList = [] # 客户端
        self.room_list = []
        self.listSocket = []

        # self.t = threading.Thread(target=self.run, args=(),)
        # self.t.setDaemon(True)
        # self.t.start()

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.localIP, self.serverPort))
        #print("连接成功!")
        server.listen(0)
        print("等待连接中……")
        while True:
            conn,addr = server.accept()#接收连接
            print("***连接成功***")
            while True:
                data = conn.recv(1024)#接收客户发来的数据
                print("接收到的命令为：",data)
                if not data:
                    print("客户断开连接")
                    break
                com = str(data,encoding="utf-8")
                msg = self.login_msg(True,com)
                conn.sendall(msg.encode('utf-8'))
        server.close()

    def make_uid(self):
        return random.randint(1,999999)

    def make_user(self,user_name):
        try:
            self.userList.append(User(user_name,make_uid(),"ground","100"))
            return True
        except:
            return False

    def login_msg(self,flag,user_name):
        msg = {
            "header" : "login",
            "msg" : "success",
            "uid" : self.make_uid(),
            "username" : user_name,
            "state" : "100",
            "in_where" : "ground",
        }
        if flag:
            return json.dumps(msg)
        else:
            msg = {
                "header" : "login",
                "msg" : "err"
            }
            return json.dumps(msg) 

    def get_list(self):
        a = {
            "room" : 
        }
        return self.room_list

a = Servers()
a.run()

