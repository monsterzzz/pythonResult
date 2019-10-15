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


# 棋盘类
class Qipan(QWidget):
    
    def __init__(self,Main_window):
        
        super().__init__() 
        self.MainWindow = Main_window
        self.start_point = (25,15)   #起始点 在QT组件的左上角
        self.line_len = 600    # 线的长度
        self.point_pos = self.get_map_pos()   # 获得所有点
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
        

    def paintEvent(self, e):  # 绘图
        qp = QPainter() 
        qp.begin(self) 
        self.drawLines(qp) 
        self.drawEllipses(qp,self.pos,self.enemy_pos)
        qp.end()
        self.qp = qp 

    def drawEllipses(self,qp,pos1,pos2): # 画圆
        if pos1['corlor'] == "black":
            qp.setBrush(QColor(0, 0, 0)) # 笔刷颜色
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
        
        

    def drawLines(self,qp):  # 画线
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
        
    def get_map_pos(self):   # 获得棋盘上的所有点
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


class WatchUI(QWidget):    # 观战类
    def __init__(self,server):
        super().__init__()
        self.ui_Window = Ui_watch()
        self.ui_Window.setupUi(self)
        self.Qipan = Qipan(self)
        self.server = server
        self.ui_Window.pushButton.clicked.connect(self.btn_click)  # 绑定事件 退出观战
        self.ui_Window.pushButton_2.clicked.connect(self.btn2_click) # 获取列表
        self.ui_Window.listWidget.itemDoubleClicked['QListWidgetItem*'].connect(self.kickout_user) # 踢人
        layout = QHBoxLayout()
        layout.addWidget(self.Qipan)
        
        self.ui_Window.qipan.setLayout(layout)

    def kickout_user(self,item):  
        text = item.text().split()
        user_name = text[0]
        uid = text[1]
        ip = text[2]
        port = text[3]
        rid = text[4]
        reply = QMessageBox.question(self,"question","you will kickout {}({}),and the room game will over,\n this window will close also!,are you sure?".format(user_name,uid),QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server.kickout(uid)
            for i in self.server.corners:
                if int(i['rid']) == int(rid):
                    i['is_watch'] = False
            self.hide()

    def btn_click(self):
        self.server.leave_watch()

    def btn2_click(self):
        all_user = self.server.get_user(is_all=True)
        self.ui_Window.listWidget_2.addItem("USER LIST :")
        self.ui_Window.listWidget_2.addItem("{:<8}{:<8}{:<8}{:<8}{:<10}".format("user_name","uid","in_where","state","addr"))
        
        for i in all_user:
            user_name = i['name']
            uid = i['uid']
            in_where = i['in_where']
            state = i['state']
            addr = "({} : {})".format(i['addr'][0],i['addr'][1])
            self.ui_Window.listWidget_2.addItem("{:<8}{:<8}{:<8}{:<8}{:<10}".format(user_name,uid,in_where,state,addr))

    def set_pos(self,pos1,pos2):   # 重新绘图
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
   

    # 自定义信号事件  通过 emit()  之后 会调用这个函数
    def signal_method(self,string):
       
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
            self.watch_qipan_update(pos1,pos2)  # 更新棋盘  传入两个坐标列表


        elif data['header'] == "GAME":   
            # 头为 GAME 的信息 说明需要关闭窗口了
            pos1 = []
            pos2 = []
            # 把所有房间的 是否被 观战 设置为False
            # 其实可以不用写for循环的，传入 房间的 rid就行了
            # 但是我生成观战类的时候没有传入 rid 现在再改有点麻烦  = = 就不改了
            for i in self.corners:
                i['is_watch'] = False
            if self.watch_ui.isVisible():
                reply = QMessageBox.information(self.watch_ui,"info",data['data'] + "\n the window will close~",QMessageBox.Yes)
                # 关闭窗口前 先把观战窗口重绘
                # 清空棋盘上面的棋子
            self.watch_qipan_update(pos1,pos2)
            # 再关闭窗口
            self.watch_ui.hide()

    def leave_watch(self):
        # 关闭观战窗口
        # 设置 是否被观战
        for i in self.corners:
            i["is_watch"] = False
        self.watch_ui.set_pos([],[])
        self.watch_ui.hide()

    def send_msg(self):
        # 把 后台窗口 发送的命令 先添加到 消息窗口上
        self.FrameUI.msg_list.addItem("COMMAND : " + self.FrameUI.lineEdit.text())
        # 先 把这个命令用 : 分割一下
        data = self.FrameUI.lineEdit.text().split(":")
        if len(data) > 1:
            # 如果 :  分割之后data 的长度 大于1 说明  是要发送消息给所有用户或者特定用户
            msg = data[1]  # 需要发送的消息
            uid = data[0].split(" ")[1] # 发送给谁
            if uid != "ALL" :   # 如果不是发给所有人
                # 在用户列表中 找到 需要发送的人 
                # 使用 其 client 发送 消息
                for user in self.userList:
                    if int(uid) == int(user['uid']):
                        message = {
                            "header" : "INFO",
                            "is_all" : False,
                            "data" : msg 
                        }
                        JsonData = (json.dumps(message) + "######").encode('utf-8')
                        user['client'].sendall(JsonData)
            else: # 如果发送给所有人
                for user in self.userList:
                    message = {
                            "header" : "INFO",
                            "is_all" : True,
                            "data" : msg 
                        }
                    JsonData = (json.dumps(message) + "######").encode('utf-8')
                    user['client'].sendall(JsonData)
        else: # 如果用 ： 分割的长度 为1 说明 : 不在命令中，也就是 不是发送消息的命令
            data = "".join(data) # 再把消息还原
            if data == "GAMES":    
                self.get_playing_game()  # 在消息窗口中列出 正在游戏中 的房间
            elif "kickout" in data:  
                self.kickout(data.split()[1]) # 踢人 把需要踢掉的人 的 uid 传入
            elif "watch" in data:
                data = data.split()  # 观战
                if len(data) == 1:   # 如果 分割长度 为1 说明没有输入 rid
                    QMessageBox.information(self.FrameWindow,"info","please enter rid",QMessageBox.Yes)
                else:  
                    rid = data[1]   
                    user1_pos = []
                    user2_pos = []
                    room_exist_flag = False
                    # 找到 需要观战的房间
                    for corner in self.corners:
                        if int(corner['rid']) == int(rid):
                            room_exist_flag = True
                            # 找到了 说明房间存在
                            if int(corner['state']) == 200:
                                # 如果 房间在 游戏中
                                self.watch_ui.show()
                                # 打开观战 窗口

                                # 观战窗口的用户列表 设置
                                self.watch_ui.ui_Window.listWidget.clear()
                                user1_info = corner['users'][0]
                                user1_str = "{} {} {} {} {}".format(user1_info['name'],user1_info['uid'],user1_info['addr'][0],user1_info['addr'][1],user1_info['in_where'])
                                user2_info = corner['users'][1]
                                user2_str = "{} {} {} {} {}".format(user2_info['name'],user2_info['uid'],user2_info['addr'][0],user2_info['addr'][1],user2_info['in_where'])
                                self.watch_ui.ui_Window.listWidget.addItem(user1_str)
                                self.watch_ui.ui_Window.listWidget.addItem(user2_str)
                                # 把该房间的 是否被观战 设置为 True
                                corner['is_watch'] = True
                                try:
                                    user1_pos = corner['users'][0]['qipan_pos']
                                except:
                                    user1_pos = []
                                try:
                                    user2_pos = corner['users'][1]['qipan_pos']
                                except:
                                    user2_pos = []
                                
                                # 更新窗口
                                self.watch_qipan_update(user1_pos,user2_pos)
                            else:
                                QMessageBox.information(self.FrameWindow,"info","the room is not playing...",QMessageBox.Yes)
                            break
                    if not room_exist_flag:  
                        QMessageBox.information(self.FrameWindow,"info","the room is not exist",QMessageBox.Yes)
            else:
                self.FrameUI.msg_list.addItem("ERROR :  ERROR COMMAND!")
                        


    def watch_qipan_update(self,pos1,pos2):
        # 更新 观战窗口 函数 
        # 对传入的列表进行处理
        # 第一个始终为黑色棋子
        # 第二个为白色棋子
        user1 = {
            "corlor" : "black",
            "pos"    :  pos1
        }
        user2 = {
            "corlor" : "white",
            "pos"    : pos2
        }
        # 更新观战 棋盘
        self.watch_ui.set_pos(user1,user2)
                
            

    def get_playing_game(self):
        # 找到正在游戏中的房间
        # state为200的房间 就是 正在游戏中
        result = []
        for corner in self.corners:
            if "state" in corner and int(corner['state']) == 200 :
                result.append(corner)
        # 往 消息窗口 添加消息
        self.FrameUI.msg_list.addItem("playing room:")
        if result:
            for i in result:
                str_message = "room_id :{} playing...".format(i['rid'])
                self.FrameUI.msg_list.addItem(str_message)
        else:
            self.FrameUI.msg_list.addItem("no room is playing")
        

    def kickout(self,uid):
        # 踢人功能
        def get_current_corner():
            for corner in self.corners:
                for user in corner['users']:
                    if int(user['uid']) == int(uid):
                        return corner
            return None
        # 因为踢人需要uid 所以从uid 找到 用户所在的房间
        current_corner = get_current_corner()

        # 如果找到了
        if current_corner:
            # 遍历当前房间的用户列表
            for user in current_corner['users']:
                # 给当前房间的所有用户发送踢人消息
                # 给客户端进行判断 被踢掉的人 是否 是 自己
                # 如果是自己 客户端 再发送退出房间的请求
                msg = {
                    "Head" : "KICKOUT",
                    "uid"  : uid,
                    "data" : "Systerm has kickout {} {}".format(user['name'],user['uid'])
                }
                JsonData = json.dumps(msg).encode('utf-8')
                self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
        else:
            QMessageBox.information(self.FrameWindow,"info","user not find",QMessageBox.Yes)
                



    def cheak_qipan(self,point,current_qipan):
        # 五子棋的胜利判定
        # 这个是判定 八个方向 八个方向 是 四条直线
        # 从最新的一个点 从一个方向出发
        # 如果这个方向下一个点 存在自己的位置信息中
        # 那么说明 这个方向下一个点是相同颜色的 再把这个点设置为当前点
        # 重复这个步骤 直到在这个方向找不到点 ，再从这个方向的相反方向寻找，这样就完成了一条直线的查找
        # 如果一条直线上存在5个点 则说明胜利
        
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
        # 获取用户列表
        # is_all 为 true 的话 就返回所有用户
        # is_all 为 false 并且 传入了 room_id 就返回 这个房间id 为 roomid 的所有用户
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
        # 查找用户的客户端 
        # 以便于发送消息
        for user in self.userList:
            if int(user['uid']) == int(uid):
                return user['client']
    
    def send_room_list_msg(self):
        # 向所有客户端发送 游戏房间 列表
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
                                    if user['in_where'] != "ground" and int(user['in_where']) == int(current_corner['rid']):
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
                        elif message['header'] == "READY": # 收到了准备消息
                            msg = {
                                "header" : "READY",
                                "uid"    : message['uid'],
                                "rid"   :message['rid'],
                            }
                            # 找到当前房间
                            for i in self.corners:
                                if int(i['rid']) == int(message['rid']):
                                    for user in i['users']:
                                        if int(user['uid']) == int(message['uid']):
                                            user['is_ready'] = True
                                            current_corner = i
                                            break
                                    break
                            # 如果当前房间的用户人数 大于1 
                            if len(current_corner['users']) > 1:
                                # 开始进行 准备 计数
                                ready_cout = 0
                                for i in current_corner['users']:
                                    if "is_ready" in i and i['is_ready']:
                                        ready_cout += 1
                                # 如果准备数 等于 2 
                                # 说明两个玩家已经准备开始游戏了
                                # 接下来就发送游戏开始的信号给客户端
                                # 并且把当前房间的状态设置为200 200就是正在游戏中
                                if ready_cout == 2:
                                    msg['data'] = "start"
                                    current_corner['state'] = 200
                                    for user in self.userList:
                                        if user['in_where'] != "ground" and int(user['in_where']) == int(message['rid']):
                                            user['state'] = "playing"
                                    self.updateUserListUI()
                                else:
                                    msg['data'] = 'wait'
                            else:
                                msg['data'] = 'wait'
                            
                            JsonData = json.dumps(msg).encode("utf-8")
                            # 向当前房间的所有用户 发送 继续等待 或者 开始游戏 的信息 
                            for i in current_corner['users']:
                                self.udpServer[self.corners.index(current_corner)].sendto(JsonData, i['addr'])

                        elif message['header'] == "RESTART":
                            # 如果收到了 重开游戏的 信息
                            if message['data'] == "request":
                                msg = {
                                    "header" : "request",
                                    "uid"   : message['uid'],
                                    "rid"   : message['rid'],
                                }
                                # 定制一个 头为 请求的 字典 准备发送给另外一个用户
                                JsonData = json.dumps(msg).encode("utf-8")
                                # 找到当前房间
                                for i in self.corners:
                                    if int(i['rid']) == int(message['rid']):
                                        current_corner = i
                                        # 找到当前房间内的另外用户
                                        # 发送请求重开的消息
                                        for user in i['users']:  
                                            if int(user['uid']) != int(message['uid']):
                                                other_user = user
                                                self.udpServer[self.corners.index(current_corner)].sendto(JsonData, user['addr'])
                                                break
                                        break
                            
                            elif message['data'] == "Yes":
                                # 收到了另外一个用户对于 请求重开的 答复
                                msg = {
                                    "header" : "RESTART",
                                    "uid"   : message['uid'],
                                    "data"   : "Yes"
                                }
                                JsonData = json.dumps(msg).encode("utf-8")
                                # 发送给当前房间的所有用户
                                for i in self.corners:
                                    if int(i['rid']) == int(message['rid']):
                                        # 如果正在被观战
                                        if "is_watch" in i and i['is_watch'] == True:
                                            game_msg = {
                                                "header" : "GAME",
                                                "data"   : "the game is restart..."
                                            }
                                            # 那么发射信号 给自定义的信号处理函数重绘并且关闭窗口
                                            self._signal.emit(json.dumps(game_msg))

                                        # 重开了 那么就把 两个用户的状态 从 playing 设置为 free
                                        for user in self.userList:
                                            if user['in_where'] != "ground" and int(user['in_where']) == int(message['rid']):
                                                user['state'] = "free"
                                        self.updateUserListUI()
                                        
                                        # 把当前房间内的所有用户的状态设置一下 
                                        # 把棋盘位置清空
                                        # 准备状态设为False
                                        for user in i['users']:  
                                            user['qipan_pos'] = []
                                            user['is_ready'] = False
                                            # 发送重开消息
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

                    except:
                        print('UDP检查到异常')

                else:
                    #tcpClient　就是客户端发送的命令
                    try:
                        # 由于TCP 会存在 粘包问题 
                        # 我后面才意识到这个问题
                        # 但是如果再修改的话 那么就很麻烦 
                        # 在这里 取巧使用了 ######  设置为包分隔符
                        # 如果粘包了 那么也有这个分隔符可以让客户端进行分割
                        addr = sock.getpeername()
                        command = sock.recv(1024)
                        #当command 为空的时候　表示客户端tcp已经断开连接了
                        command = str(command,encoding='utf-8')
                        commands = command.replace("}{","}######{").split("######")
                        for command in commands:
                            if not command:
                                continue
                            else:
                                try:
                                    command = json.loads(command)
                                except:
                                    pass
                                
                                print('TCP command:', command)
                                # 获取房间列表
                                if command["header"] == 'LIST':
                                    message = {}
                                    message['header'] = 'GAMELIST'
                                    message['data'] = self.corners
                                    JsonData = (json.dumps(message) + "######").encode('utf-8')
                                    sock.sendall(JsonData)
                                # 获取用户列表
                                elif command["header"] == 'GET':
                                    message = {}
                                    message['header'] = 'USERLIST'
                                    if command["data"] == 'all':
                                        message['data'] = self.get_user(is_all=True)
                                    else: 
                                        message['data'] = self.get_user(room_id=command["data"])
                                    JsonData = (json.dumps(message) + "######").encode('utf-8')
                                    sock.sendall(JsonData)
                                # 登录
                                elif command["header"] == 'LOGIN':
                                    message = {} 
                                    message['header'] = 'LOGIN'
                                    flag = False    # 是否重名
                                    for i in self.userList:   
                                        if i["name"] == command["msg"]: # 如果已经存在了
                                            flag = True  # 重名！
                                    if flag:
                                        message['data'] = 'error'  
                                    else:
                                        # 这里是一个用户的基本信息
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
                                    # 发送登录是否成功的消息给登录用户
                                    JsonData = (json.dumps(message) + "######").encode('utf-8')
                                    sock.sendall(JsonData)


                                    # 如果登录成功了 就发消息给所有用户
                                    # 更新用户列表
                                    if not flag:
                                        message = {}
                                        message['header'] = "USERLIST"
                                        message['data'] = self.get_user(is_all=True)
                                        JsonData = (json.dumps(message) + "######").encode('utf-8')
                                        for user in self.userList:
                                            user['client'].sendall(JsonData)

                                # 进入房间
                                elif command['header'] == 'ENTER':
                                    data = command['data']
                                    para = data.split(' ')
                                    rid = int(para[0])
                                    ip = para[1]
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
                                        # 把当前用户的in_where 设置为 当前房间的 rid
                                        for i in range(len(self.userList)):
                                            if int(self.userList[i]['uid']) == uid:
                                                self.userList[i]['in_where'] = rid

                                        # 如果当前房间人数等于2
                                        # 那么就向其它用户发送 更新用户列表的消息
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
                                                if int(i['uid']) != int(uid):
                                                    msg = {
                                                        "header" : "CORLOR"
                                                    }
                                                    msg['data'] = "black"
                                                    msg['turn'] = True
                                                    JsonData = json.dumps(msg).encode("utf-8")
                                                    user_client = self.get_user_client(i['uid'])
                                                    user_client.sendall(JsonData)
                                                    break
                                            break
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
                                    msg = {
                                        "header" : "GAME",
                                        "data" : "user exit the room!"
                                    }
                                    self._signal.emit(json.dumps(msg))
                                
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

                                elif command['header'] == "INVITE":
                                    if command['data'] == "request":
                                        msg = {
                                            "header" : "INVITE",
                                            "data"   : "request",
                                            "state"   : "success"
                                        }
                                        flag = False
                                        for i in self.userList:
                                            if int(i['uid']) == int(command['to']):
                                                if i['in_where'] == "ground":
                                                    invite_msg = {
                                                        "header" : "INVITE",
                                                        "data"   : "invite",
                                                        "from"   : command['from'],
                                                        "rid"   : command['rid']
                                                    }
                                                    JsonData = json.dumps(invite_msg).encode('utf-8')
                                                    i['client'].sendall(JsonData)
                                                    flag = True
                                                break
                                        if flag:
                                            JsonData = json.dumps(msg).encode('utf-8')
                                            sock.sendall(JsonData)
                                        else:
                                            msg['state'] = "fail"
                                            JsonData = json.dumps(msg).encode('utf-8')
                                            sock.sendall(JsonData)
                                    elif command['data'] == "Yes":
                                        msg = {
                                            "header" : "INVITE",
                                            "data"   : "Yes",
                                            "user_name" : command['user_name'],
                                            "uid"   : command['uid']
                                        }
                                        for i in self.userList:
                                            if int(i['uid']) == int(command['to']):
                                                JsonData = json.dumps(msg).encode('utf-8')
                                                i['client'].sendall(JsonData)
                                                break
                                    elif command['data'] == "No":
                                        msg = {
                                            "header" : "INVITE",
                                            "data"   : "No",
                                            "user_name" : command['user_name'],
                                            "uid"   : command['uid']
                                        }
                                        for i in self.userList:
                                            if int(i['uid']) == int(command['to']):
                                                JsonData = json.dumps(msg).encode('utf-8')
                                                i['client'].sendall(JsonData)
                                                break


                                            
                    except BaseException as e:
                        traceback.print_exc()
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
            #title = '{:<15}{:<6}{:5}{:10}'.format(user['name'],str(user['uid']),user['state'],user['in_where'])
            title = '{:<10}{:<6}{:10}{:10}'.format(user['name'],str(user['uid']),user['in_where'],user['state'])
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
