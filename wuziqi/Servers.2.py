import select
import socket
import threading
import random
import time
import re
import json
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *  
from PyQt5.QtGui import *

from serverui import *
from watch import *
import traceback 



class Qipan(QWidget):
    
    def __init__(self,Main_window):
        
        super().__init__() 
        self.MainWindow = Main_window
        self.start_point = (25,15)
        self.line_len = 600
        self.point_pos = self.get_map_pos()
        self.pos = {
            "corlor" : "",
            "pos" : ""
        }
        self.enemy_pos = {
            "corlor" : "",
            "pos" : ""
        }
        self.initUI() 
        
    def initUI(self): 
        self.setGeometry(300, 300, 800, 700) 
        

    def paintEvent(self, e): 
        qp = QPainter() 
        qp.begin(self) 
        self.drawLines(qp) 
        self.drawEllipses(qp,self.pos,self.enemy_pos)
        qp.end()
        self.qp = qp 

    def drawEllipses(self,qp,pos1,pos2):
        if pos1['corlor'] == "black":
            qp.setBrush(QColor(0, 0, 0))
            for i in pos1['pos']:
                qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
            qp.setBrush(QColor(255, 255, 255))
            for i in pos2['pos']:
                qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
        else:
            qp.setBrush(QColor(255, 255, 255))
            for i in pos1['pos']:
                qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
            qp.setBrush(QColor(0, 0, 0))
            for i in pos2['pos']:
                qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
        
        

    def drawLines(self,qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine) 
        qp.setPen(pen) 
        start_point = self.start_point
        start_x = start_point[0]
        start_y = start_point[1]
        x_len = 600
        y_len = 600 
        for i in range(15):
            qp.drawLine(start_x,start_y,start_x + x_len - x_len / 15,start_y)
            start_y += y_len / 15
        start_x = start_point[0]
        start_y = start_point[1]
        for i in range(15):
            qp.drawLine(start_x,start_y,start_x,start_y + x_len - y_len / 15)
            start_x +=  y_len / 15
        
    def get_map_pos(self):
        result = []
        x = self.start_point[0]
        y = self.start_point[1]
        for i in range(15):
            for j in range(15):
                current_pos = [x,y]
                result.append( current_pos )
                y += int(self.line_len / 15)
            x += int(self.line_len / 15)
            y = self.start_point[1]
        return result


class WatchUI(QWidget):
    def __init__(self,server):
        super().__init__()
        self.ui_Window = Ui_watch()
        self.ui_Window.setupUi(self)
        self.Qipan = Qipan(self)
        self.server = server
        self.ui_Window.pushButton.clicked.connect(self.btn_click)
        self.ui_Window.pushButton_2.clicked.connect(self.btn_click)
        layout = QHBoxLayout()
        layout.addWidget(self.Qipan)
        
        self.ui_Window.qipan.setLayout(layout)

    def btn_click(self):
        self.father_frame.Client.leave_watch()

    def btn_2_click(self):
        corner = self.father_frame.Client.find_playing_room()
        self.ui_Window.listWidget_2.addItem("playing room ： ")
        for i in corner:
            self.ui_Window.listWidget_2.addItem(i)

    def btn_3_click(self):
        user = self.father_frame.Client.get_user(is_all=True)
        for i in user:
            self.ui_Window.listWidget_2.addItem(i)

    def set_pos(self,pos1,pos2):
        self.Qipan.pos = pos1
        self.Qipan.enemy_pos = pos2
        self.Qipan.update()


class Server(QObject):
    _signal = pyqtSignal(str)
    def __init__(self,UI):
        super().__init__()
        self.FrameUI = UI.ui_Window
        self.FrameWindow = UI
        self.localIP = '127.0.0.1'
        self.serverPort = 5000
        #self.corners = ()
        self.watch_ui = WatchUI(self)
        self.corners = []
        self.udpServer = [] # corner socket
        self.userList = [] # 客户端
        self.listSocket = []
        self.ground_people = []
        self._signal.connect(self.signal_method)
        self.play_room = []
        self.buildServer()
        self.t = threading.Thread(target=self.run, args=(),)
        self.t.setDaemon(True)
        self.t.start()

        #self.openCorner('Coner1','English')
        #self.openCorner('Coner2', 'Chinese')

        #self.updateCornerListUI()

    def signal_method(self,string):
        print("************")
        print(string)
        data = json.loads(string)
        if data['header'] == "POS":
            try:
                pos1 = data['data'][0]['qipan_pos']
            except:
                pos1 = []
            try:
                pos2 = data['data'][1]['qipan_pos']
            except:
                pos2 = []
            print("############################")
            print(pos1,pos2)
            print("########################")
            self.watch_qipan_update(pos1,pos2)
        elif data['header'] == "GAME":
            pos1 = []
            pos2 = []
            reply = QMessageBox.information(self.watch_ui,"info",data['data'] + "\n the window will close~",QMessageBox.Yes)
            self.watch_qipan_update(pos1,pos2)
            self.watch_ui.hide()

            

    def find_playing_room(self):
        result = []
        for i in self.corners:
            if int(i['state']) == 200:
                result.append(i)
        return result

    def send_msg(self):
        data = self.FrameUI.lineEdit.text().split(":")
        if len(data) > 1:
            msg = data[1]
            uid = data[0].split(" ")[1]
            if uid != "ALL" :
                for user in self.userList:
                    if int(uid) == int(user['uid']):
                        message = {
                            "header" : "INFO",
                            "is_all" : False,
                            "data" : msg 
                        }
                        JsonData = (json.dumps(message) + "######").encode('utf-8')
                        user['client'].sendall(JsonData)
            else:
                for user in self.userList:
                    message = {
                            "header" : "INFO",
                            "is_all" : True,
                            "data" : msg 
                        }
                    JsonData = (json.dumps(message) + "######").encode('utf-8')
                    user['client'].sendall(JsonData)
        else:
            data = "".join(data)
            if data == "GAMES":
                self.get_playing_game()
            elif "kickout" in data:
                self.kickout(data.split()[1])
            elif "watch" in data:
                data = data.split()
                if len(data) == 1:
                    QMessageBox.information(self.FrameWindow,"info","please enter rid",QMessageBox.Yes)
                else:
                    rid = data[1]
                    user1_pos = []
                    user2_pos = []
                    room_exist_flag = False
                    for corner in self.corners:
                        if int(corner['rid']) == int(rid):
                            room_exist_flag = True
                            if int(corner['state']) == 200:
                                self.watch_ui.show()
                                corner['is_watch'] = True
                                try:
                                    user1_pos = corner['users'][0]['qipan_pos']
                                except:
                                    user1_pos = []
                                try:
                                    user2_pos = corner['users'][1]['qipan_pos']
                                except:
                                    user2_pos = []
                                

                                self.watch_qipan_update(user1_pos,user2_pos)
                            else:
                                QMessageBox.information(self.FrameWindow,"info","the room is not playing...",QMessageBox.Yes)
                            break
                    if not room_exist_flag:  
                        QMessageBox.information(self.FrameWindow,"info","the room is not exist",QMessageBox.Yes)
                        


    def watch_qipan_update(self,pos1,pos2):
        user1 = {
            "corlor" : "black",
            "pos"    :  pos1
        }
        user2 = {
            "corlor" : "white",
            "pos"    : pos2
        }
        self.watch_ui.set_pos(user1,user2)
                
            

    def get_playing_game(self):
        result = []
        for corner in self.corners:
            if "state" in corner and int(corner['state']) == 200 :
                result.append(corner)
        return result



    def kickout(self,uid):
        for corner in self.corners:
            for user in corner['users']:
                msg = {
                    "Head" : "KICKOUT",
                    "uid"  : uid,
                    "data" : "Systerm has kickout {} {}".format(user['name'],user['uid'])
                }
                JsonData = json.dumps(msg).encode('utf-8')
                self.udpServer[self.corners.index(corner)].sendto(JsonData, user['addr'])
                



    def cheak_qipan(self,point,current_qipan):
        x,y = point[0],point[1]

        current_pos = [x,y]
        point_cout = 1
        while True:
            if [current_pos[0] - 40,current_pos[1]] in current_qipan:
                current_pos = [current_pos[0] - 40,current_pos[1]]
                point_cout += 1
            else:
                break
        current_pos = [x,y]
        while True:
            if [current_pos[0] + 40,current_pos[1]] in current_qipan:
                current_pos = [current_pos[0] + 40,current_pos[1]]
                point_cout += 1
            else:
                break
        if point_cout >= 5:
            return True
        
        
        current_pos = [x,y]
        point_cout = 1
        while True:
            if [current_pos[0],current_pos[1] - 40 ] in current_qipan:
                current_pos = [current_pos[0],current_pos[1]  - 40]
                point_cout += 1
            else:
                break
        current_pos = [x,y]
        while True:
            if [current_pos[0],current_pos[1] + 40 ] in current_qipan:
                current_pos = [current_pos[0] ,current_pos[1] + 40]
                point_cout += 1
            else:
                break
        if point_cout >= 5:
            return True
        

        x,y = point[0],point[1]
        current_pos = [x,y]
        point_cout = 1
        while True:
            if [current_pos[0] - 40 ,current_pos[1] - 40 ] in current_qipan:
                current_pos = [current_pos[0] - 40,current_pos[1]  - 40]
                point_cout += 1
            else:
                break
        current_pos = [x,y]
        while True:
            if [current_pos[0] + 40 ,current_pos[1] + 40 ] in current_qipan:
                current_pos = [current_pos[0] + 40,current_pos[1]  + 40]
                point_cout += 1
            else:
                break
        if point_cout >= 5:
            return True

        
        current_pos = [x,y]
        point_cout = 1
        while True:
            if [current_pos[0] - 40 ,current_pos[1] + 40 ] in current_qipan:
                current_pos = [current_pos[0] - 40,current_pos[1]  + 40]
                point_cout += 1
            else:
                break
        current_pos = [x,y]
        while True:
            if [current_pos[0] + 40 ,current_pos[1] - 40 ] in current_qipan:
                current_pos = [current_pos[0] + 40,current_pos[1]  - 40]
                point_cout += 1
            else:
                break
        if point_cout >= 5:
            return True

        return False
        
    
    

    def get_user(self,is_all = False,room_id = None):
        result = []
        if is_all:
            for i in self.userList:
                user = {
                    "name" : i['name'],
                    "uid"  : i['uid'],
                    "state" : i["state"],
                    "in_where" : i["in_where"],
                    "addr" : i['addr']
                }
                result.append(user)
        else:
            for i in self.userList:
                if i['in_where'] != "ground":
                    if int(i['in_where']) == int(room_id):
                        user = {
                            "name" : i['name'],
                            "uid"  : i['uid'],
                            "state" : i["state"],
                            "in_where" : i["in_where"],
                            "addr" : i['addr']
                        }
                        result.append(user)
        return result


    def get_user_client(self,uid):
        for user in self.userList:
            if int(user['uid']) == int(uid):
                return user['client']
    
    def send_room_list_msg(self):
        for i in self.userList:
            message = {}
            message['header'] = 'GAMELIST'
            message['data'] = self.corners
            JsonData = (json.dumps(message) + "######").encode('utf-8')
            i['client'].sendall(JsonData)

    def run(self):
        # self.buildServer()
        print('Server OnListen')
        while self.listSocket:
            #有数据可读的时候，select返回(可能描述不是很准确)
            rlist, wlist, elist = select.select(self.listSocket, [], [])
            if not (rlist or wlist or elist):
                print ('time out')
                break
            for sock in rlist:
                #如果是tcpServer表示有新的客户端向我们发送连接请求了
                if sock is self.tcpServer:
                    print ('connecting ...')
                    try:
                        client, addr = sock.accept()
                        print ('TCP connect from', addr)
                        client.setblocking(False)
                        # #将新的客户端添加到listSocket,这样就可以被select检测了
                        self.listSocket.append(client)
                        # flg = True
                        # for user in self.userList:
                        #     if addr == user[0]:
                        #         flg = False
                        #         break
                        # if flg: # 不在列表中
                        #     self.userList.append((addr,client))
                        #self.updateUserListUI()
                    except Exception:
                        print ('exit threading')
                        break
                elif sock in self.udpServer:
                    try:
                        #udp　表示用户发送的聊天消息
                        data, addr = sock.recvfrom(1024)
                        print ('UDP recvfrom ', data, ' from', addr)
                        data = str(data,encoding="utf-8")
                        message = json.loads(data)
                        if message['header'] == "pos": # 如果发送的是位置信息 说明游戏已经开始
                            msg = {
                                    "header" : "POS",   # 制定回复消息头
                                    }
                            # 从房间列表里面 找到当前房间的用户列表
                            for corner in self.corners:
                                for user in corner['users']:
                                    print(int(user['uid']) == int(message['uid']),user['uid'],message['uid'])
                                    if int(user['uid']) == int(message['uid']):
                                        current_corner = corner
                                        current_user = corner['users']
                                        break
                            # 从用户列表里面找到 发送消息的用户 把这个用户的位置信息修改为发送过来的位置信息
                            for user in current_user:
                                if int(user['uid']) == int(message['uid']):
                                    user['qipan_pos'] = message['Data']
                            # 信息修改完成 把回复消息的数据 修改为 这个房间内所有用户的信息 信息里面包含用户的各种信息 
                            # 包括位置信息
                            msg['data'] = current_user
                            # 向房间内的所有用户发送 消息
                            for user in current_user:
                                JsonData = json.dumps(msg).encode("utf-8")
                                self.udpServer[self.corners.index(corner)].sendto(JsonData, user['addr'])
                            if "is_watch" in current_corner and current_corner['is_watch'] == True:
                                 self._signal.emit(json.dumps(msg))
                            # 检查当前用户的位置 是否达到了胜利条件
                            flag = self.cheak_qipan(message['Data'][-1],message['Data'])
                            # 如果胜利
                            if flag:
                                # 修改当前房间用户的位置信息 以及 准备状态
                                current_corner['state'] = 100
                                for user in current_user:
                                    user['is_ready'] = False
                                    user['qipan_pos'] = []
                                for user in self.userList:
                                    if user['in_where'] != "ground" and int(user['in_where']) == int(message['rid']):
                                        user['state'] = "free"
                                self.updateUserListUI()

                                # 找到当前用户 
                                for user in current_user:
                                    if int(user['uid']) == int(message['uid']):
                                        break
                                # 把消息写入 游戏消息 消息头为 GAME
                                game_msg = {
                                    "header" : "GAME",
                                    "data"   : "winner is {} {}".format(user['name'],user['uid'])
                                }
                                # 向房间内的所有用户发送胜利消息
                                JsonData = json.dumps(game_msg).encode("utf-8")
                                for user in current_user:
                                    self.udpServer[self.corners.index(corner)].sendto(JsonData, user['addr'])
                                if "is_watch" in current_corner and current_corner['is_watch'] == True:
                                     self._signal.emit(json.dumps(game_msg))
                        elif message['header'] == "READY":
                            msg = {
                                "header" : "READY",
                                "uid"    : message['uid'],
                                "rid"   :message['rid'],
                            }
                            for i in self.corners:
                                if int(i['rid']) == int(message['rid']):
                                    for user in i['users']:
                                        if int(user['uid']) == int(message['uid']):
                                            user['is_ready'] = True
                                            current_corner = i
                                            print("888888888888",current_corner)
                                            break
                                    break
                            print("99999999999",current_corner)
                            if len(current_corner['users']) > 1:
                                print("*******",current_corner)
                                print("$$%########")
                                print(current_corner['users'])
                                ready_cout = 0
                                for i in current_corner['users']:
                                    print("!!!!!",i)
                                    if "is_ready" in i and i['is_ready']:
                                        ready_cout += 1
                                if ready_cout == 2:
                                    msg['data'] = "start"
                                    current_corner['state'] = 200
                                    for user in self.userList:
                                        if user['in_where'] != "ground" and int(user['in_where']) == int(message['rid']):
                                            user['state'] = "playing"
                                    self.updateUserListUI()
                                            
                                    self.play_room.append(current_corner)
                                else:
                                    msg['data'] = 'wait'
                            else:
                                msg['data'] = 'wait'
                            
                            JsonData = json.dumps(msg).encode("utf-8")
                            for i in current_corner['users']:
                                self.udpServer[self.corners.index(current_corner)].sendto(JsonData, i['addr'])

                        elif message['header'] == "RESTART":
                            if message['data'] == "request":
                                msg = {
                                    "header" : "request",
                                    "uid"   : message['uid'],
                                    "rid"   : message['rid'],
                                }
                                JsonData = json.dumps(msg).encode("utf-8")
                                for i in self.corners:
                                    if int(i['rid']) == int(message['rid']):
                                        current_corner = i
                                        for user in i['users']:  
                                            if int(user['uid']) != int(message['uid']):
                                                other_user = user
                                                self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
                                                break
                                        break
                            
                            elif message['data'] == "Yes":
                                msg = {
                                    "header" : "RESTART",
                                    "uid"   : message['uid'],
                                    "data"   : "Yes"
                                }
                                JsonData = json.dumps(msg).encode("utf-8")
                                for i in self.corners:
                                    if int(i['rid']) == int(message['rid']):
                                        if "is_watch" in i and i['is_watch'] == True:
                                            game_msg = {
                                                "header" : "GAME",
                                                "data"   : "the game is restart..."
                                            }
                                            self._signal.emit(json.dumps(game_msg))

                                        for user in self.userList:
                                            if user['in_where'] != "ground" and int(user['in_where']) == int(message['rid']):
                                                user['state'] = "free"
                                        self.updateUserListUI()
                                            
                                        for user in i['users']:  
                                            user['qipan_pos'] = []
                                            user['is_ready'] = False
                                            self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
                            else:
                                msg = {
                                    "header" : "RESTART",
                                    "uid"   : message['uid'],
                                    "data"   : "No"
                                }
                                JsonData = json.dumps(msg).encode("utf-8")
                                for i in self.corners:
                                    if int(i['rid']) == int(message['rid']):
                                        for user in i['users']:  
                                            self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
                                   
                            

                                

                            # if message['data'] == "Yes":
                            #     for i in self.corners:
                            #         if int(i['rid']) == int(message['rid']):
                            #             for user in i['users']:  
                            #                 current_corner = i
                            #                 user['qipan_pos'] = [] 
                            #                 user['is_ready'] = False
                                                                         

                        
                            # for user in current_corner['users']:
                            #     if int(user['uid']) != int(message['uid']):
                            #         JsonData = json.dumps(message).encode("utf-8")
                            #         self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
                            #         break
                                     
                           
                            
                        elif message['To'] =='all':
                            # 全部转发
                            for corner in self.corners:
                                if addr in corner['users']:
                                    print('Room {0} recice message:{1} From:{2}'.format(corner['name'], data, addr))
                                    # 将消息转发
                                    for user in corner['users']:
                                        # message = {}
                                        # message['From'] = addr
                                        # message['Data'] = data
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user)
                        else:
                            for corner in self.corners:
                                if addr in corner['users']:
                                    user = (message['To'][0],message['To'][1])
                                    JsonData = json.dumps(message).encode('utf-8')
                                    self.udpServer[self.corners.index(corner)].sendto(JsonData, user)
                        #将消息发送到所以客户机上，转发
                        # for key, value in self.clientInfo.items():
                        #     sock.sendto(data, value)

                    except:
                        print('UDP检查到异常')
                        traceback.print_exc()
                        #print()
                        # self.listSocket.remove(sock)

                else:
                    #tcpClient　就是客户端发送的命令
                    try:
                        addr = sock.getpeername()
                        command = sock.recv(1024)
                        #当command 为空的时候　表示客户端tcp已经断开连接了
                        command = str(command,encoding='utf-8')
                        try:
                            command = json.loads(command)
                        except:
                            pass
                        print('TCP command:', command)
                        if command == 'GET':
                            message = {}
                            message['header'] = 'GAMELIST'
                            message['data'] = self.corners
                            JsonData = (json.dumps(message) + "######").encode('utf-8')
                            sock.sendall(JsonData)
                        elif command["header"] == 'GET':
                            message = {}
                            message['header'] = 'USERLIST'
                            #print(self.userList)
                            if command["data"] == 'all':
                                message['data'] = self.get_user(is_all=True)
                            else: 
                                message['data'] = self.get_user(room_id=command["data"])
                            print("*****")
                            print(message)
                            JsonData = (json.dumps(message) + "######").encode('utf-8')
                            sock.sendall(JsonData)
                            # for user in self.userList:
                            #     user['client'].sendall(JsonData)
                            #sock.sendall(JsonData)
                        elif command["header"] == 'LOGIN':
                            message = {}
                            message['header'] = 'LOGIN'
                            flag = False
                            for i in self.userList:
                                if i["name"] == command["msg"]:
                                    flag = True
                            if flag:
                                message['data'] = 'error'
                            else:
                                user = {
                                    "name" : command["msg"],
                                    "uid"  : random.randint(1,99999),
                                    "addr" : addr,
                                    "state" : "free",
                                    "in_where" : "ground",
                                    "client" : client
                                }
                                self.userList.append(user)
                                message['data'] = 'success'
                                message['user_name'] = user["name"]
                                message["uid"] = user['uid']
                                message['in_where'] = user['in_where']
                                self.updateUserListUI()
                            JsonData = (json.dumps(message) + "######").encode('utf-8')
                            sock.sendall(JsonData)

                            if not flag:
                                message = {}
                                message['header'] = "USERLIST"
                                message['data'] = self.get_user(is_all=True)
                                JsonData = (json.dumps(message) + "######").encode('utf-8')
                                for user in self.userList:
                                    user['client'].sendall(JsonData)


                        elif command['header'] == 'ENTER':
                            data = command['data']
                            para = data.split(' ')
                            rid = int(para[0])
                            ip = para[1]
                            port = para[2]
                            port = int(para[2])
                            user_name = para[3]
                            uid = int(para[4])
                            # 房间 用户列表 添加用户
                            for corner in self.corners:
                                if int(corner['rid']) == rid:
                                    user = {
                                        "name": user_name,
                                        "uid" : uid,
                                        "addr" : (ip,port),
                                        "in_where" : rid
                                    }
                                    msg = {
                                        "header" : "ENTER",
                                        "rid" : rid
                                    }
                                    if len(corner['users']) >= 2:
                                        msg['data'] = "fail"
                                        flag = False
                                    else:
                                        msg['data'] = "success"
                                        flag = True
                                        current_corner = corner
                                        self.corners[self.corners.index(corner)]['users'].append(user)
                                    JsonData = (json.dumps(msg) + "######").encode('utf-8')
                                    user_client = self.get_user_client(uid)
                                    user_client.sendall(JsonData)
                                    break

                            # 如果进入成功
                            if flag:
                                for i in range(len(self.userList)):
                                    if int(self.userList[i]['uid']) == uid:
                                        self.userList[i]['in_where'] = rid
                                print(self.userList)
                                if len(corner['users']) == 2:
                                    other_user = current_corner['users'][0]
                                    user_msg = {
                                        "header" : "USERLIST",
                                        "data"   : self.get_user(room_id=rid)
                                    }
                                    JsonData = (json.dumps(user_msg) + "######").encode('utf-8')
                                    self.get_user_client(other_user['uid']).sendall(JsonData)
                                msg = {
                                    "header" : "CORLOR"
                                }
                                if len(current_corner['users']) > 1:
                                    msg['data'] = "white"
                                    msg['turn'] = False
                                else:
                                    msg['data'] = "black"
                                    msg['turn'] = True
                                JsonData = (json.dumps(msg) + "######").encode('utf-8') 
                                user_client.sendall(JsonData)
                                # 向所有在大厅的用户 发送 新的用户列表信息
                                for user in self.userList:
                                    if user['in_where'] == "ground":
                                        msg = {
                                            "header" : "USERLIST",
                                            "data"   : self.get_user(is_all=True)
                                        }
                                        
                                        JsonData = (json.dumps(msg) + "######").encode('utf-8')
                                        user['client'].sendall(JsonData)

                                self.updateUserListUI()
                                self.send_room_list_msg()

                                
                                
                            # 转发进入消息 UDP
                            for corner in self.corners:
                                if int(rid) == int(corner['rid']):
                                    # 将消息转发
                                    for user in corner['users']:
                                        message = {
                                            "header" : "INFO"
                                        }
                                        message['data'] = '[Systerm message] {}({})  {}:{} Enter Room {}.'.format(user_name,uid,ip,port,rid)
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user['addr'])

                        elif command['header'] == 'QUIT': # 退出聊天室命令
                            command = command['data']
                            para = command.split(' ')
                            rid = para[0]
                            user_name = para[1]
                            uid = para[2]
                            ip = para[3]
                            port = int(para[4])
                            for corner in self.corners:
                                if int(corner['rid']) == int(rid): 
                                    for i in self.corners[self.corners.index(corner)]['users']:
                                        if int(i['uid']) == int(uid):
                                            for item in self.userList:
                                                if int(item['uid']) == int(uid):
                                                    item['in_where'] = "ground"
                                                    item['state'] = "free"
                                                    self.updateUserListUI()
                                                    break
                                            break
                                        
                                    for user in self.corners[self.corners.index(corner)]['users']:
                                        user['is_ready'] = False
                                        message = {
                                            "header" : "QUIT_INFO",
                                            'uid'    : uid,
                                            "data"   : user_name,
                                            "rid"    : rid
                                        }
                    
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user['addr'])
                                    self.corners[self.corners.index(corner)]['users'].remove(i) 
                                    
                                    break
                                    
                            message = {}
                            message['header'] = 'USERLIST'
                            # sock.sendall(JsonData)
                            for user in self.userList:
                                try:
                                    if int(user['in_where']) == int(rid):
                                        message['data'] = self.get_user(room_id=rid)
                                        JsonData = (json.dumps(message) + "######").encode('utf-8')
                                        user['client'].sendall(JsonData)
                                    else:
                                        message['data'] = self.get_user(is_all=True)
                                        JsonData = (json.dumps(message) + "######").encode('utf-8')
                                        user['client'].sendall(JsonData)
                                except:
                                    pass
                            self.send_room_list_msg()
                        
                        elif command['header'] == 'EXIT': # 退出游戏命令
                            command = command['data']
                            para = command.split(' ')
                            name = para[0]
                            uid = para[1]
                            ip = para[2]
                            port = int(para[3])
                            self.listSocket.remove(sock)
                            for user in self.userList:
                                if int(uid) == user['uid']:
 
                                    msg = {
                                        "header" : "EXIT",
                                        "data"  : "success"
                                    }
                                    JsonData = (json.dumps(msg) + "######").encode('utf-8')
                                    user['client'].sendall(JsonData)
                                    self.userList.remove(user)
                                    break

                            
                            for i in self.userList:
                                msg = {
                                    "header" : "USERLIST",
                                    "data" : self.get_user(is_all = True)
                                }
                                JsonData = (json.dumps(msg) + "######").encode('utf-8')
                                i['client'].sendall(JsonData)

                            self.updateUserListUI()
                            print('Exit From ', addr)
                    except BaseException as e:
                        print("error",e)
                        print("line : ",traceback.print_exc())
                        if sock in self.listSocket:
                            self.listSocket.remove(sock)
                            addr = sock.getpeername()
                        for user in self.userList:
                            if addr == user['addr']:
                                self.userList.remove(user)
                        self.updateUserListUI()
                        print('远程主机强迫关闭了一个现有的连接')
        print ('out threading')
        self.tcpServer.close()

    def updateUserListUI(self):
        self.FrameUI.listWidget.clear()
        for user in self.userList:
            title = '{:<15}{:<6}{:5}{:10}'.format(user['name'],str(user['uid']),user['state'],user['in_where'])
            self.FrameUI.listWidget.addItem(title)

    def updateCornerListUI(self):
        self.FrameUI.room_list.clear()
        for corner in self.corners:
            title = '{:<10}{:<10}(Port:{:<5})'.format(corner['rid'],corner['state'],corner['port'])
            self.FrameUI.room_list.addItem(title)

    def buildServer(self):
        try:
            # tcp服务器建立
            self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpServer.setblocking(False)
            self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 服务器地址绑定
            self.tcpServer.bind((self.localIP, self.serverPort))
            self.tcpServer.listen(0)
            # select 输入可读参数，意思是当这个列表里面任何一个元素可读，select就有返回值
            self.listSocket.append(self.tcpServer)
            # for server in self.udpServer:
            #     self.listSocket.append(server)
        except:
            self.status = False
        else:
            self.status = True

    def openCorner(self,rid):
        # udp的端口是tcp端口号+1
        udpPort = random.randint(3000, 6000)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.bind((self.localIP, udpPort))
        udpServer.setblocking(False)
        corner = {}
        corner['rid'] = rid
        corner['state'] = "100"
        corner['port'] = udpPort
        corner['users'] = []
        self.corners.append(corner)
        self.udpServer.append(udpServer)
        self.listSocket.append(udpServer)# 加入监听
        print('Add Corner:({rid}:{host},{port})'.format(rid = rid,host = self.localIP , port = udpPort))
        message = {}
        message['header'] = 'GAMELIST'
        message['data'] = self.corners
        JsonData = (json.dumps(message) + "######").encode('utf-8')
        for user in self.userList:
            # JsonData = json.dumps(self.corners).encode('utf-8')
            user['client'].sendall(JsonData)
        return corner

    def userEixt(self,addr):
        for user in self.userList:
            if addr == user[0]:
                self.listSocket.remove(user[1])
                self.userList.remove(user)
                message = {}
                message['header'] = 'EXIT SERVER'
                message['data'] = self.corners
                JsonData = (json.dumps(message) + "######").encode('utf-8')
                user['addr'].sendall(JsonData)
                self.updateUserListUI()
                break

    def roomEixt(self,rid):
        for corner in self.corners:
            if int(corner['rid']) == int(rid):
                # 通知所有用户
                sock = self.udpServer[self.corners.index(corner)]
                for user in corner['users']:
                    message = {
                        "header" : "CLOSE",
                        "data"   : '[System Message] Corner is closed!.',
                        "rid"    :  rid
                    }
                    JsonData = json.dumps(message).encode('utf-8')
                    sock.sendto(JsonData, user['addr'])
                self.corners.remove(corner)
                # 通知所有客户端
                message = {}
                message['header'] = 'GAMELIST'
                message['data'] = self.corners
                JsonData = (json.dumps(message) + "######").encode('utf-8')
                for user in self.userList:
                    try:
                        if int(user["in_where"]) == int(rid):
                            user["in_where"] = "ground"
                        user['client'].sendall(JsonData)
                    except:
                        pass
                self.listSocket.remove(sock) # 监听取消
                self.udpServer.remove(sock)
                self.updateCornerListUI()
                break
        pass

    def close(self):
        print('Close Server')
        self.listSocket = []
        self.tcpServer.close()
        time.sleep(1)

class ServerWindowDlg(QMainWindow):
    def __init__(self):
        super(ServerWindowDlg, self).__init__()
        self.ui_Window = Ui_MainWindow()
        self.ui_Window.setupUi(self)
        self.server = Server(self)
        self.ui_Window.listWidget.itemDoubleClicked['QListWidgetItem*'].connect(self.add_content)
        self.ui_Window.room_list.itemDoubleClicked['QListWidgetItem*'].connect(self.cornerClose)
        self.ui_Window.pushButton_2.clicked.connect(self.NewCorner)
        self.ui_Window.pushButton.clicked.connect(self.server.send_msg)
        if self.server.status:
            self.ui_Window.state.setText('On Listen')
            self.ui_Window.address.setText(self.server.localIP)
            self.ui_Window.port.setText(str(self.server.serverPort))
        else:
            self.ui_Window.state.setText('Open Error')

    def closeEvent(self, *args, **kwargs):
        self.server.close()

    def add_content(self,item):
        data = item.text().split()
        uid = data[1]
        self.ui_Window.lineEdit.setText("to {}: ".format(uid))

    def NewCorner(self):
        rid = self.ui_Window.room_id.text()
        if rid and rid.isdigit():
            flag = True
            for i in self.server.corners:
                if int(i['rid']) == int(rid):
                    flag = False
                    break
            if flag:
                self.server.openCorner(rid)
                self.server.updateCornerListUI()
            else:
                QMessageBox.information(self,"info","has been exits")
        else:
            QMessageBox.information(self,"info","only number and can't be null")
        

    def cornerClose(self,item):
        corner = item.text()
        reply = QMessageBox.question(self, '提示',
                                     'Are you sure to Destory {0}?'.format(corner),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            rid = corner.split()[0].strip()
            self.server.roomEixt(rid)
        else:
            pass

if __name__ =='__main__':
    app = QApplication(sys.argv)
    mainWindow = ServerWindowDlg()
    mainWindow.show()
    sys.exit(app.exec_())
