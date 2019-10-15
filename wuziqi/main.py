from ui_m import Ui_MainWindow
from h import Ui_Dialog 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *  
import sys
import socket
import threading
import os
import json
import select

class Main_window(QMainWindow):
    signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui_Window = Ui_MainWindow()
        self.ui_Window.setupUi(self)
  
    def handle_click(self):
        if not self.isVisible():
            self.show()

class Client:
    def __init__(self,Login_window,MainWindow):
        
        self.MainWindow = MainWindow
        self.MainFrame = MainWindow.ui_Window # UI 界面

        self.llll = Login_window
        self.login_window = Login_window.ui_Window


        self.localIP = '127.0.0.1' # 本机IP

        self.host = '127.0.0.1' # 服务器IP
        self.port = 5000

        self.current_corner_name = ''  # 当前聊天室名字
        self.udpSocket = None # 当前聊天室socket
        self.udpPort = 0 # 当前聊天室Port
        self.room = None # 当前聊天室对象

        self.socket_list = [] #监听列表
        self.corners = [] # 聊天室
        self.bulid_tcp()
        # self.userListInCorners = []
        # 获取房间列表
        #self.getList()

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
                            self.MainFrame.label_2.setText('Failure')
                            self.MainFrame.pushButton.setEnabled(False)
                            signal.emit('MessageBox')
                            # self.tcpSocket.close()
                        else:
                            print(data)
                            #print(str(data,encoding="utf-8"))
                            data = str(data,encoding="utf-8")
                            message = json.loads(data)
                            if message['Head'] == 'CORNERSLIST':
                                self.corners = message['Data']
                                print(self.corners)
                                self.updateCornersList()
                            if message['Head'] == 'USERLIST' and message['Corner'] == self.current_corner_name:
                                userList = message['Data']
                                self.MainFrame.listWidget_3.clear()
                                for user in userList:
                                    title = '{}:{}'.format(user[0],user[1])
                                    self.MainFrame.listWidget_3.addItem(title)
                            if message['Head'] == 'EXIT SERVER':
                                print('Disconnected from chat server')
                                self.tcpSocket.shutdown(socket.SHUT_RDWR)
                                self.tcpSocket = None
                                self.socket_list = []
                                self.MainFrame.label_2.setText('Failure')
                                self.MainFrame.pushButton.setEnabled(False)
                                signal.emit('MessageBox')
                            if message['Head'] == 'LOGIN':
                                if message['Data'] == "success":
                                    #
                                    #self
                                    #self.MainWindow.handle_click()
                                    self.llll.accept()
                                    
                                    #self.llll.hide()
                                    #
                                    #self.llll.close()
                                    
                                #self.corners = message['Data']
                                #print(self.corners)
                                #self.updateCornersList()
                else:
                    # UDP datas
                    try:
                        data = sock.recv(4096)
                    except:
                        pass
                    else:
                        # addr = sock.getpeername()
                        data = str(data,encoding="utf-8")
                        print('UDP recive: {data}'.format(data = data ) )
                        message = json.loads(data)
                        if message['To'] !='all':
                            str_message = '[Private] {}:{}：   {}'.format(message['From'][0],message['From'][1],message['Data'])
                        else:
                            str_message = '[All] {}:{}：   {}'.format(message['From'][0], message['From'][1],
                                                                        message['Data'])
                        self.MainFrame.listWidget.addItem(str_message)
                        if message['Data'] =='Corner is closed!.':
                            self.room = None
                            self.socket_list.remove(self.udpSocket)
                            self.udpSocket = None

    def getList(self):
        print('Sending Messages GET')
        self.tcpSocket.sendall(b'GET')

    def login(self):
        print("Sending Messages LOGIN")
        msg = {
            "header" : "LOGIN",
            "msg" : self.login_window.lineEdit.text(),
        }
        self.tcpSocket.sendall(bytes(json.dumps(msg),encoding="utf-8"))

class Login_window(QDialog):
    signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui_Window = Ui_Dialog()
        self.next_window = Main_window()
        #self.signal.connect(self.messagebox)
        self.ui_Window.setupUi(self)
        self.Client = Client(self,self.next_window)
        #print(self)
    
    def messagebox(self):
        pass
    # def login_btn(self):
    #     t = threading.Thread(target=self.Client.login, args=(self.ui_Window.user_name.text(),),)
    #     t.setDaemon(True)
    #     t.start()
    #     t.join()
    #     #creat_c.run()
    #     if self.Client.msg["header"] == "login" and self.Client.msg["msg"] == "success":
    #         self.next_window.handle_click()
    #         self.next_window.ui_Window.user_name.setText(self.Client.msg["username"])
    #         self.hide()
    #         self.close()
    #     else:
    #         print("@!")
    
    def closeEvent(self, event):
        #self.next_window.handle_click()
        #self.close_signal.emit()
        self.close()

        

if __name__ =='__main__':
    app = QApplication(sys.argv)
    loginWindow = Login_window()
    #print(login)
    loginWindow.ui_Window.pushButton.clicked.connect(loginWindow.Client.login)
    if loginWindow.exec_() == QDialog.Accepted:
        loginWindow.next_window.show()
    
    
    #loginWindow.show()

        sys.exit(app.exec_())




