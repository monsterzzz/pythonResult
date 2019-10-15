from ui_m import Ui_MainWindow
from h import Ui_Dialog 
from invite_ui import Ui_Dialog as inviteui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *  
from PyQt5.QtGui import *
import sys
import socket
import threading
import os
import json
import select
import random
import time

# 棋盘类
# 这个棋盘类和服务端的棋盘类差不多
# 服务端的棋盘类没有响应鼠标事件
class Qipan(QWidget):

    def __init__(self,Main_window):
        
        super().__init__() 
        #self.father = father
        self.MainWindow = Main_window
        self.start_point = (25,15)
        self.line_len = 600
        self.point_pos = self.get_map_pos()
        self.pos = []
        self.is_start = False
        self.color = None
        self.enemy_pos = []
        self.is_my_turn = False
        self.initUI() 
        #self.show()

    def initUI(self): 
        self.setGeometry(300, 300, 800, 700) 
       
        pass

    def paintEvent(self, e): 
        qp = QPainter() 
        qp.begin(self) 
        self.drawLines(qp) 
        self.drawEllipses(qp,self.pos,self.enemy_pos)
        qp.end()
        self.qp = qp 

    def drawEllipses(self,qp,self_pos,enemy_pos):
        if self.color:
            if self.color == "black":
                qp.setBrush(QColor(0, 0, 0))
                for i in self_pos:
                    qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
                qp.setBrush(QColor(255, 255, 255))
                for i in enemy_pos:
                    qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
            else:
                qp.setBrush(QColor(255, 255, 255))
                for i in self_pos:
                    qp.drawEllipse(i[0] - 10 ,i[1] - 10,20,20)
                qp.setBrush(QColor(0, 0, 0))
                for i in enemy_pos:
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

    def mousePressEvent(self,event):
        pos = [event.x(),event.y()]
        if self.MainWindow.Client.room:
            if not self.is_start:
                QMessageBox.information(self.MainWindow, '提示', 'You must wait..')
            else:
                if not self.is_my_turn:
                    QMessageBox.information(self.MainWindow, '提示', 'it is not your turn')
                else:
                    for i in self.point_pos:
                        if pos[0] + 20 >= i[0] and pos[0] - 20 <= i[0] and pos[1] + 20 >= i[1] and pos[1] - 20 <= i[1] :
                            if i not in self.pos and i not in self.enemy_pos:
                                self.pos.append(i)
                                self.MainWindow.Client.game_pos(self.pos)
                            else:
                                print("ERROR : pos has been append")

                            break
        else:
            QMessageBox.information(self.MainWindow, '提示', 'You need to enter Room first.')


class InviteUI(QDialog):
    def __init__(self,Main_window):
        super().__init__() 
        self.Window = inviteui()
        self.Window.setupUi(self)
        self.MainWindow = Main_window
        self.Window.pushButton.clicked.connect(self.send_invite)
    
    def send_invite(self):
        line_text = self.Window.lineEdit.text()
        if line_text.isdigit():
            self.MainWindow.Client.invite_user(line_text)
        else:
            QMessageBox.information(self,"warning","input can't be null and only number")


# 主窗口类
class Main_window(QMainWindow):
    signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui_Window = Ui_MainWindow()
        self.ui_Window.setupUi(self)
        self.Client = Client(self)    # 窗口类的客户端
        self.login_window = Login_window(self)
        self.current_room = "ground"   # 当前房间名
        self.invite_window = InviteUI(self)
        self.ui_Window.room_list_view.itemDoubleClicked['QListWidgetItem*'].connect(self.enter_room) # 双击链接函数
        self.ui_Window.ready_btn.clicked.connect(self.ready) # 准备按钮
        self.ui_Window.restart_btn.clicked.connect(self.restart) # 重开按钮
        self.ui_Window.ready_btn.hide()  # 刚开始没有进入房间 所以隐藏准备按钮与重开按钮
        self.ui_Window.restart_btn.hide()
        self.ui_Window.invite_btn.hide()
        self.ui_Window.invite_btn.clicked.connect(lambda : self.invite_window.show())
        self.ui_Window.login_btn.clicked.connect(self.open_login_window) # 登录按钮
        self.ui_Window.exit_btn.clicked.connect(self.quit_room)  # 退出按钮
        self.Qipan = Qipan(self) # 初始化棋盘
        #self.Qipan = Qipan(self.ui_Window.groupBox_2) 
        layout = QHBoxLayout()      
        layout.addWidget(self.Qipan)
        
        self.ui_Window.groupBox_2.setLayout(layout)  # 把棋盘画到主窗口上
    

    # 重开 调用客户端的重开函数
    def restart(self):
        self.Client.restart()
    
    # 重写关闭窗口事件
    def closeEvent(self, *args, **kwargs):
        if self.Client.socket_list:
            self.Client.quit_room()
    
    # 进入房间 调用客户端的进入房间函数
    def enter_room(self,item):
        room_name = item.text()
        room_id = room_name.split()[1]
        self.Client.enter_room(room_id)
    # 退出房间 调用客户端的 退出房间函数
    def quit_room(self):
        self.Client.quit_room()

    # 打开登录窗口 
    def open_login_window(self):
        self.login_window.show()

    # 点击准备按钮 的函数
    def ready(self):
        self.Client.ready()

    # 重开按钮
    def restart(self):
        self.Client.restart()


# 登录窗口
class Login_window(QDialog):
    def __init__(self,father_frm):
        super().__init__()
        self.ui_Window = Ui_Dialog()
        self.ui_Window.setupUi(self)
        self.father_frame = father_frm  # 设置其父组件， 父组件就是主窗口类
        #self.Client = Client
        self.ui_Window.pushButton.clicked.connect(self.btn_click) # 点击登录按钮的函数
        
    def btn_click(self):
        name = self.ui_Window.lineEdit.text()   # 获取输入框的内容
        self.father_frame.Client.login(name)   # 调用客户端的登录
   
class Room():
    def __init__(self,name,socket,server):
        self.name = name
        self.socket = socket
        self.server = server

    def sendMessage(self,text):
        marchtObj = re.match(r'@(.*?):(.*?):(.*?)',text,re.S|re.M)
        message = {}
        message['From'] = self.socket.getsockname()
        if marchtObj:
            message['To'] = (marchtObj.group(1),int(marchtObj.group(2)))
            message['Data'] = text[len(marchtObj.group(0)):]
        else:
            message['To'] = 'all'
            message['Data'] = text
        JsonData = json.dumps(message).encode('utf-8')
        try:
            print('Sending Messages:{} '.format(message))
            self.socket.sendto(JsonData, self.server)
        except:
            print('发送失败!')
            return False
        return True

    # 发送 当前位置列表信息
    def game_pos(self,uid,pos):
        message = {
            "header" : "pos",
            "Data"  : pos,
            "uid"    : uid
        }
        JsonData = json.dumps(message).encode("utf-8")
        try:
            print('Sending Messages:{} '.format(message))
            self.socket.sendto(JsonData, self.server)
        except:
            print('发送失败!')
            return False
    # 发送 准备信息
    def ready_stauts(self,data):
        print("Sending Message: {}".format(data))
        self.socket.sendto(data,self.server)
    # 发送重开信息
    def restart(self,data):
        print("Sending Message: {}".format(data))
        self.socket.sendto(data,self.server)

# 客户端类
class Client(QObject):
    #_signal= QtCore.pyqtSignal(str)
    _signal = pyqtSignal(str)  #自定义信号
    def __init__(self,MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.MainFrame = MainWindow.ui_Window # UI 界面

        self.localIP = '127.0.0.1' # 本机IP
        self.user_name = "" # 用户名
        self.uid = ""       # 用户id 服务端分配的标识符
        self.host = '127.0.0.1' # 服务器IP
        self.port = 5000 
        #self.lll = Login_window
        self.current_corner_name = 'ground'  # 当前聊天室名字
        self.udpSocket = None # 当前聊天室socket
        self.udpPort = 0 # 当前聊天室Port
        self.room = None # 当前聊天室对象
        self.login_stauts = False
        self.socket_list = [] #监听列表
        self.corners = [] # 聊天室
        self._signal.connect(self.my_method) # 自定义信号连接的自定义函数
        self.is_ready = False  # 当前是否准备
        self.bulid_tcp()   #建立TCP连接
    
    # 自定义信号触发的函数
    def my_method(self,string):
        message = json.loads(string)
        # 如果 header 是 request，就是从服务端转发过来的对手的重开请求
        if "header" in message and message['header'] == "request":
            reply = QMessageBox.question(self.MainWindow,"restart","enemy request restart , are you acctecp?",QMessageBox.Yes|QMessageBox.No)
            msg = {
                "header" : "RESTART",
                "uid" : message['uid'],
                'rid' : message['rid']
            }
            # 如果点击了 YEs 说明接受重开
            if reply == QMessageBox.Yes:
                msg['data'] = "Yes"
            else:
                msg['data'] = "No"
            JsonData = json.dumps(msg).encode("utf-8")
            # 发送是否接受
            self.room.restart(JsonData)
        # 如果 header 是 RESTART
        # 如果 data 是 Yes 说明接受了重开
        # 把客户端的棋盘信息都还原为 未开始游戏时的状态
        elif "header" in message and message['header'] == "RESTART":
            if message['data'] == "No":
                if int(message["uid"]) == int(self.uid):
                    QMessageBox.information(self.MainWindow,"info","enemy refuse",QMessageBox.Yes)
            elif message['data'] == "Yes":
                if int(message["uid"]) == int(self.uid):
                    QMessageBox.information(self.MainWindow,"info","enemy allow",QMessageBox.Yes)
                self.MainWindow.Qipan.pos = []
                self.MainWindow.Qipan.enemy_pos = []
                self.MainWindow.Qipan.is_start = False
                self.MainFrame.ready_btn.show()
        # 如果 header 是 QUIT， 那么说明有退出游戏事件发生
        elif "header" in message and message['header'] == "QUIT":
            # 退出了游戏 ，那么该房间的游戏就应该终止
            # 游戏停止了，就把所有状态还原
            self.MainWindow.Qipan.pos = []
            self.MainWindow.Qipan.enemy_pos = []
            data = message['data']
            QMessageBox.information(self.MainWindow,"info",data,QMessageBox.Yes)
            self.MainWindow.Qipan.update()
            self.MainFrame.ready_btn.show()
            self.MainWindow.Qipan.is_start = False
            self.is_ready = False
        # 如果 header 是GAME 说明 游戏结束了
        # 游戏结束也就应该还原所有状态
        elif "header" in message and message['header'] == "GAME":
            self.MainWindow.Qipan.pos = []
            self.MainWindow.Qipan.enemy_pos = []
            self.MainWindow.Qipan.is_start = False   
            self.MainFrame.ready_btn.show()
            self.is_ready = False    
            data = message['data']
            QMessageBox.information(self.MainWindow,"info",data,QMessageBox.Yes)
            self.MainFrame.msg_list.addItem(data)
            self.MainWindow.Qipan.update()
        elif "header" in message and message['header'] == "INVITE":
            from_id = message['from'] 
            to_room = message['rid']
            str_message = "uid为 {} 的用户邀请您进入 {} 房间一起游戏,\n是否接受请求?".format(from_id,to_room)
            reply = QMessageBox.question(self.MainWindow.invite_window,"邀请请求",str_message,QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.Yes:
                msg = {
                    "header" : "INVITE",
                    "data"  : "Yes",
                    "user_name" : self.user_name,
                    "uid" : self.uid,
                    "to"  : message['from']
                }
                JsonData = json.dumps(msg).encode('utf-8')
                self.tcpSocket.sendall(JsonData)
                self.enter_room(to_room)
            else:
                msg = {
                    "header" : "INVITE",
                    "data"  : "No",
                    "user_name" : self.user_name,
                    "uid" : self.uid,
                    "to"  : message['from']
                }
                JsonData = json.dumps(msg).encode('utf-8')
                self.tcpSocket.sendall(JsonData)
                
        elif "header" in message and message['header'] == "INVITE_REQUEST":
            if message['data'] == "success":
                QMessageBox.information(self.MainWindow.invite_window,"info","邀请成功！",QMessageBox.Yes)
            else:
                str_message = "邀请失败,被邀请用户不存在或者不在大厅！"
                QMessageBox.information(self.MainWindow.invite_window,"info",str_message,QMessageBox.Yes)

        elif "header" in message and message['header'] == "INVITE_STATE":
            try:
                QMessageBox.information(self.MainWindow.invite_window,"info",message['data'],QMessageBox.Yes)
                self.MainWindow.invite_window.hide()
            except:
                QMessageBox.information(self.MainWindow,"info",message['data'],QMessageBox.Yes)

    def invite_user(self,uid):
        msg = {
            "header" : "INVITE",
            "data"  : "request",
            "from"  : self.uid,
            "to" : uid,
            "rid" : self.current_corner_name
        }
        JsonData = json.dumps(msg).encode("utf-8")
        self.tcpSocket.sendall(JsonData)
    # 重新开始
    def restart(self):
        msg = {
            "header" : "RESTART",
            "rid"   : self.current_corner_name,
            "uid"   : self.uid,
            "data"  : "request"
        }
        JsonData = json.dumps(msg).encode("utf-8")
        self.room.restart(JsonData)

    # 准备
    def ready(self):
        msg = {
            "header" : "READY",
            "rid"   : self.current_corner_name,
            "uid"   : self.uid
        }
        JsonData = json.dumps(msg).encode("utf-8")
        self.room.ready_stauts(JsonData)
        
    # 建立TCP连接
    def bulid_tcp(self):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# 服务器连接
        self.tcpSocket.settimeout(3)
        try:
            self.tcpSocket.connect((self.host, self.port))
        except socket.error as e:
            print('Unable to connect')
            self.status = False
            self.tcpSocket = None
            #self.MainFrame.pushButton.setEnabled(False)
            #self.login_window.label_3.setText('Failure')
            # exit(0)
        else:
            print('Connected to remote host')
            self.status = True
            #self.login_window.label_3.setText('Successed')
            # 开启监听
            self.socket_list.append(self.tcpSocket)
            self.t = threading.Thread(target=self.run, args=(self.MainWindow.signal,),)
            self.t.setDaemon(True)
            self.t.start()
    # 监听 sock 接收的消息
    def run(self,signal):
        while self.socket_list:
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(self.socket_list, [], [])
            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.tcpSocket:
                    try:
                        data = sock.recv(4096)
                    except:
                        print('TCP Error')
                    else:
                        if not data:
                            print('Disconnected from chat server')
                            self.tcpSocket.shutdown(socket.SHUT_RDWR)
                            self.tcpSocket = None
                            self.socket_list = []
                            #self.MainFrame.label_2.setText('Failure')
                            #self.MainFrame.pushButton.setEnabled(False)
                            #signal.emit('MessageBox')
                            # self.tcpSocket.close()
                        else:
                            # 服务端定义了分隔符 防止粘包
                            data = str(data,encoding="utf-8").split("######")
                            # 如果粘包了 这样就可以分开两个包
                            # 如果没有粘包， 会有一个空字符串在分割出来的列表里面
                            for i in data:
                                if not i: #如果是空字符串 就跳过
                                    pass
                                else:
                                    print("TCP recive:",i)
                                    message = json.loads(i)

                                    if message['header'] == 'GAMELIST': # 游戏房间列表
                                        self.corners = message['data']
                                        self.updateCornersList()

                                    if message['header'] == 'ENTER': # 进入房间是否成功
                                        if message['data'] == "success" : # 如果成功
                                            self.MainFrame.invite_btn.show()  # 显示邀请按钮
                                            self.get_uesr_list(message['rid']) # 发送获取该房间用户的列表
                                            self.MainFrame.room_name.setText(str(message['rid'])) # 把主窗口的房间标题修改
                                            self.current_corner_name = str(message['rid']) # 修改当前客户端的房间名 用来退出时判断
                                            self.MainFrame.restart_btn.show()  # 进入房间成功 就应该显示准备和重开按钮
                                            self.MainFrame.ready_btn.show()  # 准备和重开按钮是重叠在一起的
                                        else:  # 进入房间失败
                                            str_message = "[Systerm message] Enter room {} fail".format(message['rid']) # 往消息窗口添加失败消息
                                            self.MainFrame.msg_list.addItem(str_message) 

                                    if message['header'] == "INFO":   # 服务端的消息 信息 向所有人 或者 特定的人
                                        if message['is_all']:  
                                            str_message = "[Systerm message] [All] {}".format(message['data'])
                                        else:
                                            str_message = "[Systerm message] [Pritive] {}".format(message['data']) # 服务端已经写好向谁发送私聊信息了，这里不用再判断
                                        self.MainFrame.msg_list.addItem(str_message)  #往消息窗口添加消息
                                    if message['header'] == 'USERLIST':  # 用户列表信息
                                        userList = message['data']
                                        self.MainFrame.current_room_list.clear() # 清空用户列表
                                        for user in userList:
                                            title = '{:<10}{:<10}{:<10}{:<10}{:<10}'.format(user['name'],user['uid'],user['addr'][0],user['addr'][1],user["in_where"])
                                            self.MainFrame.current_room_list.addItem(title) #往用户列表窗口添加消息
                                    if message['header'] == 'EXIT SERVER':  # 退出游戏 也就是退出整个程序
                                        print('Disconnected from chat server')
                                        self.tcpSocket.shutdown(socket.SHUT_RDWR)
                                        self.tcpSocket = None
                                        self.socket_list = []
                                        self.MainFrame.label_2.setText('Failure')
                                        self.MainFrame.pushButton.setEnabled(False)
                                        _signal.emit('MessageBox') 
                                    if message['header'] == "CORLOR":# 进入房间后 的 棋盘初始化 信息
                                        self.MainWindow.Qipan.color = message['data'] # 设置当前客户端的颜色
                                        self.MainWindow.Qipan.is_my_turn = message['turn'] # 是否是先手
                                    if message['header'] == 'LOGIN':  # 登录消息
                                        if message['data'] == "success": # 成功
                                            self.login_stauts == True   # 设置各种状态
                                            self.MainWindow.login_window.close()
                                            self.MainFrame.user_name.setText(message['user_name'])
                                            self.user_name = message['user_name']
                                            self.uid = message['uid']
                                            self.MainFrame.room_name.setText(message['in_where'])
                                            self.MainFrame.login_btn.hide()
                                            self.getList()   # 登录成功 就应该获取游戏房间列表
                                    if message['header'] == "INVITE":
                                        if message['data'] == "request":
                                            if message['state'] == "success":
                                                msg = {
                                                    "header" : "INVITE_REQUEST",
                                                    "data"   : "success"
                                                }
                                                self._signal.emit(json.dumps(msg))
                                            else:
                                                msg = {
                                                    "header" : "INVITE_REQUEST",
                                                    "data"   : "fail"
                                                }
                                                self._signal.emit(json.dumps(msg))
                                        elif message['data'] == "Yes":
                                            msg = {
                                                "header" : "INVITE_STATE",
                                                "data"   : "{}({}) accepted invite request".format(message['user_name'],message['uid'])
                                            }
                                            self._signal.emit(json.dumps(msg))
                                        elif message['data'] == "No":
                                            msg = {
                                                "header" : "INVITE_STATE",
                                                "data"   : "{}({}) refuse invite request".format(message['user_name'],message['uid'])
                                            }
                                            self._signal.emit(json.dumps(msg))
                                        elif message['data'] == "invite":
                                            self._signal.emit(json.dumps(message))
                                    if message['header'] == 'EXIT':  # 退出
                                        print('Disconnected from chat server')  #
                                        self.tcpSocket.shutdown(socket.SHUT_RDWR)
                                        self.tcpSocket = None
                                        self.socket_list = []
                                        self.MainWindow.close()
                                        #self.MainFrame.label_2.setText('Failure')
                                        #self.MainFrame.pushButton.setEnabled(False)
                                        #signal.emit('MessageBox')

                else:
                    # UDP datas
                    try:
                        data = sock.recv(4096)
                    except:
                        pass
                    else:
                        # addr = sock.getpeername()
                        data = str(data,encoding="utf-8")   # udp 不会粘包
                        print('UDP recive: {data}'.format(data = data ) )
                        message = json.loads(data) 
                        if "header" in message and message['header'] == "POS":   # 如果是返回了位置信息
                            data = message['data']
                            # 设置棋盘的位置信息
                            for i in data: 
                                if int(i['uid']) == int(self.uid):
                                    if "qipan_pos" in i:
                                        self.MainWindow.Qipan.pos = i["qipan_pos"] 
                                    else:
                                        self.MainWindow.Qipan.pos = []
                                else:
                                    if "qipan_pos" in i:
                                        if self.MainWindow.Qipan.enemy_pos != i["qipan_pos"]:
                                            self.MainWindow.Qipan.enemy_pos = i["qipan_pos"]
                                            self.MainWindow.Qipan.is_my_turn = True
                                        else:
                                            self.MainWindow.Qipan.is_my_turn = False
                                    else:
                                        self.MainWindow.Qipan.enemy_pos = []
                                        self.MainWindow.Qipan.is_my_turn = False
                            self.MainWindow.Qipan.update() # 更新棋盘
                        elif "header" in message and message['header'] == "INFO":  # upd 消息 信息
                            data = message['data']
                            self.MainFrame.msg_list.addItem(data)  # 消息窗口 添加消息
                        elif "header" in message and message['header'] == "QUIT_INFO":  # 游戏房间退出信息
                            # 服务端没有判断是哪个客户端退出 
                            # 只是转发退出信息
                            # 客户端自己判断 是否是自己退出
                            if int(message['uid']) != int(self.uid):
                                self.MainFrame.msg_list.addItem("{}:{} quit room {}".format(message['data'],message['uid'],message['rid']))
                                if self.MainWindow.Qipan.is_start:
                                    msg = {
                                        "header" : "QUIT",
                                        "data"   : "enemy {}:{} quit this room,the game will be restart".format(message['data'],message['uid'])
                                    }
                                    self._signal.emit(json.dumps(msg))
                            else:
                                self.current_corner_name = "ground"
                                self.MainFrame.ready_btn.hide()
                                self.MainFrame.restart_btn.hide()
                        elif "header" in message and message['header'] == "GAME":
                            self._signal.emit(json.dumps(message))  # GAME 的头信息 说明游戏结束
                        elif "Head" in message and message['Head'] == "KICKOUT": # 被踢的信息
                            # 客服端自己判断是否是自己被踢出
                            if int(message['uid']) == int(self.uid): # 如果是自己被踢出房间
                                self.quit_room()
                                str_message = "[Systerm message] Systerm has been kickout you"
                                self.MainFrame.msg_list.addItem(str_message)
                            else:
                                str_message = message['data']
                                self.MainFrame.msg_list.addItem(str_message)
                                msg = {
                                    "header" : "GAME",
                                    "data" : "user kickouted"
                                }
                                self._signal.emit(json.dumps(msg))
                        elif "header" in message and message['header'] == "CLOSE": # 房间被关闭
                            self.quit_room()
                            self.getList()
                            self.get_uesr_list("all")
                        elif "header" in message and message['header'] == "READY": # 准备消息返回
                            # 会返回游戏是否开始 或者是 要求用户继续等待 对手准备 或者 对手进入房间并准备
                            if message['data'] == "start":   # 游戏开始
                                self.MainWindow.Qipan.is_start = True # 棋盘开始 
                                self.MainFrame.ready_btn.hide()  # 开始了就隐藏准备按钮
                                self.MainFrame.restart_btn.show()  # 显示重开按钮
                            else:
                                self.MainWindow.Qipan.is_start = False
                        elif "header" in message and message['header'] == "request": 
                            # 判断是否重开 ，如果重开则设定各种信息
                            # 因为不能在子线程创建窗口 或者 更新窗口
                            # 所以使用自定义信号 发送到主线程进行打开新窗口操作
                            self._signal.emit(json.dumps(message))
                        elif "header" in message and message['header'] == "RESTART":
                            self._signal.emit(json.dumps(message))
                        elif message['To'] !='all':
                            str_message = '[Private] {}:{}：   {}'.format(message['From'][0],message['From'][1],message['Data'])
                        else:
                            str_message = '[All] {}:{}：   {}'.format(message['From'][0], message['From'][1],
                                                                        message['Data'])
                        # self.MainFrame.msg_list.addItem(str_message)
                        # if message['Data'] =='Corner is closed!.':
                        #     self.room = None
                        #     self.socket_list.remove(self.udpSocket)
                        #     self.udpSocket = None 

    def game_pos(self,pos):  # 发送位置消息
        self.room.game_pos(self.uid,pos)

    def getList(self):   # 发送获取房间列表消息
        print('Sending Messages GET')
        msg = {
            "header" : "LIST"
        }
        JsonData = json.dumps(msg).encode("utf-8")
        self.tcpSocket.sendall(JsonData)

    def get_uesr_list(self,where):  # 发送 获取 用户列表信息
        print('Sending Messages GET_user_list')
        msg = {
            "header" : "GET",
            "data" : where  # 哪里的用户 是ground 或者其他
        }
        self.tcpSocket.sendall(bytes(json.dumps(msg),encoding="utf-8"))  # 发送消息

    def login(self,user_name):  # 登录逻辑
        print("Sending Messages LOGIN")
        msg = {
            "header" : "LOGIN",   #
            "msg" : user_name,
        }
        self.tcpSocket.sendall(bytes(json.dumps(msg),encoding="utf-8"))

    def quit_room(self):
        if self.current_corner_name == "ground":
            self.quit_app()
        else:
            print('Quit Room: ' + self.current_corner_name)
            msg = {
                "header" : "QUIT",
                "data" : '{name} {user_name} {uid} {ip} {port}'.format(name= self.current_corner_name,user_name = self.user_name,uid = self.uid ,ip=self.localIP, port=self.udpPort)
            }
            #self.MainFrame.current_room_list.clear() # 清空消息列表
        
            self.tcpSocket.sendall(json.dumps(msg).encode('utf-8'))
            #self.get_uesr_list("ground")
            self.current_corner_name = "ground"
            self.MainFrame.room_name.setText("ground")
            self.socket_list.remove(self.udpSocket)
            self.udpSocket = None
            self.get_uesr_list("all")
            self.MainFrame.ready_btn.hide()
            self.MainFrame.restart_btn.hide()
            self.MainFrame.invite_btn.hide()
            self.MainWindow.Qipan.pos = []
            self.MainWindow.Qipan.enemy_pos = []
            self.MainWindow.Qipan.is_start = False
            self.room = None
            self.MainWindow.Qipan.update()
            time.sleep(1)
        
    
    def quit_app(self):
        print('Sending Messages EXIT')
        self.socket_list = []
        if self.tcpSocket != None:
            message = {
                "header" : "EXIT",
                "data"   : '{name} {uid} {ip} {port}'.format(name = self.current_corner_name, uid = self.uid,ip= self.localIP, port= self.udpPort)
            }
            self.tcpSocket.sendall(json.dumps(message).encode('utf-8'))
        

    def enter_room(self,room_id):
        name = room_id
        # 进入房间前先退出前一个
        if self.udpSocket != None:
            if name != self.current_corner_name:
                reply = QMessageBox.information(self.MainWindow, '提示', 'You need to quit Room first.')
            return self.current_corner_name
                
        
        if name != self.current_corner_name:
            print('Enter Room: ' + name)
            self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udpPort = random.randint(3000, 6000)
            self.udpSocket.bind((self.localIP, self.udpPort))
            self.current_corner_name = name
            self.socket_list.append(self.udpSocket) # 加入监听

            for corner in self.corners:
                if corner['rid'] == name:
                    self.serverUdpAddr = (self.host, corner['port'])
                    message = {
                        "header" : "ENTER",
                        "data" : '{name} {ip} {port} {user_name} {uid}'.format(name = name,ip = self.localIP,port = self.udpPort,user_name=self.user_name,uid=self.uid)
                    }
                    self.tcpSocket.sendall(bytes(json.dumps(message),encoding = "utf-8"))
                    self.room = Room(name,self.udpSocket,self.serverUdpAddr)
                    return self.room
        else:
            return self.room
        


    def updateCornersList(self):
        self.MainFrame.room_list_view.clear() # 英语角列表
        for corner in self.corners:
            title = '{:<10s}{:<10s}{:<2}'.format("room",corner['rid'],len(corner['users']))
            self.MainFrame.room_list_view.addItem(title)




if __name__ =='__main__':
    app = QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())
    # if main_window.login_window.exec_() == QDialog.accepted():
    #     main_window.show()
    #     sys.exit(app.exec_())




