import select
import socket
import threading
import random
import time
import json
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget, QMessageBox,QTableWidgetItem
from ServerMainUI import *

class Server():
    def __init__(self,UI):
        self.FrameUI = UI

        self.localIP = '127.0.0.1'
        self.serverPort = 5000
        #self.corners = ()
        self.corners = []
        self.udpServer = [] # corner socket
        self.userList = [] # 客户端
        self.listSocket = []

        self.buildServer()
        self.t = threading.Thread(target=self.run, args=(),)
        self.t.setDaemon(True)
        self.t.start()

        self.openCorner('Coner1','English')
        self.openCorner('Coner2', 'Chinese')

        self.updateCornerListUI()

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
                        #将新的客户端添加到listSocket,这样就可以被select检测了
                        self.listSocket.append(client)
                        flg = True
                        for user in self.userList:
                            if addr == user[0]:
                                flg = False
                                break
                        if flg: # 不在列表中
                            self.userList.append((addr,client))
                        self.updateUserListUI()
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
                        if message['To'] =='all':
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
                        # self.listSocket.remove(sock)

                else:
                    #tcpClient　就是客户端发送的命令
                    try:
                        addr = sock.getpeername()
                        command = sock.recv(1024)
                        print ('TCP command:', command)
                        #当command 为空的时候　表示客户端tcp已经断开连接了
                        command = str(command,encoding='utf-8')
                        if command == 'GET':
                            message = {}
                            message['Head'] = 'CORNERSLIST'
                            message['Data'] = self.corners
                            JsonData = json.dumps(message).encode('utf-8')
                            sock.sendall(JsonData)
                        elif command.find('ENTER') != -1:
                            para = command.split(' ')
                            name = para[1]
                            ip = para[2]
                            port = int(para[3])
                            for corner in self.corners:
                                if corner['name'] == name:
                                    # corner['users'].append(addr)
                                    # corner['users'].append((ip,int(port)))
                                    self.corners[self.corners.index(corner)]['users'].append((ip,port))
                                    break
                            message = {}
                            message['Head'] = 'USERLIST'
                            message['Corner'] = name
                            for corner in self.corners:
                                if corner['name'] == name:
                                    message['Data'] = corner['users']
                                    break
                            JsonData = json.dumps(message).encode('utf-8')
                            # sock.sendall(JsonData)
                            for user in self.userList:
                                user[1].sendall(JsonData)
                            # 转发进入消息 UDP
                            for corner in self.corners:
                                if name == corner['name']:
                                    # 将消息转发
                                    for user in corner['users']:
                                        message = {}
                                        message['From'] = ('System Message','0')
                                        message['To'] = 'all'
                                        message['Data'] = '{}:{} Enter Room {}.'.format(ip,port,name)
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user)
                        elif command.find('QUIT') != -1: # 退出聊天室命令
                            para = command.split(' ')
                            name = para[1]
                            ip = para[2]
                            port = int(para[3])
                            for corner in self.corners:
                                if corner['name'] == name:
                                    self.corners[self.corners.index(corner)]['users'].remove((ip,port))
                                    for user in self.corners[self.corners.index(corner)]['users']:
                                        message = {}
                                        message['From'] = ('System Message','0')
                                        message['To'] = 'all'
                                        message['Data'] = '{}:{} Exit Room.'.format(ip,port)
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user)
                                    break
                            message = {}
                            message['Head'] = 'USERLIST'
                            message['Corner'] = name
                            for corner in self.corners:
                                if corner['name'] == name:
                                    message['Data'] = corner['users']
                                    break
                            JsonData = json.dumps(message).encode('utf-8')
                            # sock.sendall(JsonData)
                            for user in self.userList:
                                user[1].sendall(JsonData)
                        elif command.find('EXIT')!=-1:
                            para = command.split(' ')
                            name = para[1]
                            ip = para[2]
                            port = int(para[3])
                            # sock.close()
                            self.listSocket.remove(sock)
                            for corner in self.corners:
                                if name == corner['name']:
                                    if (ip, port) in corner['users']:
                                        self.corners[self.corners.index(corner)]['users'].remove((ip, port))
                                    for user in self.corners[self.corners.index(corner)]['users']:
                                        message = {}
                                        message['From'] = ('System Message','0')
                                        message['To'] = 'all'
                                        message['Data'] = '{}:{} Exit Room.'.format(ip,port)
                                        JsonData = json.dumps(message).encode('utf-8')
                                        self.udpServer[self.corners.index(corner)].sendto(JsonData, user)
                                    break
                            message = {}
                            message['Head'] = 'USERLIST'
                            message['Corner'] = name
                            for corner in self.corners:
                                if corner['name'] == name:
                                    message['Data'] = corner['users']
                                    break
                            JsonData = json.dumps(message).encode('utf-8')
                            # sock.sendall(JsonData)
                            for user in self.userList:
                                user[1].sendall(JsonData)
                            # 列表更新
                            for user in self.userList:
                                if addr == user[0]:
                                    self.userList.remove(user)
                            self.updateUserListUI()
                            print('Exit From ', addr)
                    except:
                        self.listSocket.remove(sock)
                        addr = sock.getpeername()
                        for user in self.userList:
                            if addr == user[0]:
                                self.userList.remove(user)
                        self.updateUserListUI()
                        print('远程主机强迫关闭了一个现有的连接')
        print ('out threading')
        self.tcpServer.close()

    def updateUserListUI(self):
        self.FrameUI.listWidget.clear()
        for user in self.userList:
            title = '{0}:{1}'.format(user[0][0],user[0][1])
            self.FrameUI.listWidget.addItem(title)

    def updateCornerListUI(self):
        self.FrameUI.listWidget_2.clear()
        for corner in self.corners:
            title = '{:<10s}(Langue:{:<10s}, Port:{:<5d})'.format(corner['name'],corner['langue'],corner['port'])
            self.FrameUI.listWidget_2.addItem(title)

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

    def openCorner(self,name,langue):
        # udp的端口是tcp端口号+1
        udpPort = random.randint(3000, 6000)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.bind((self.localIP, udpPort))
        udpServer.setblocking(False)
        corner = {}
        corner['name'] = name
        corner['langue'] = langue
        corner['port'] = udpPort
        corner['users'] = []
        self.corners.append(corner)
        self.udpServer.append(udpServer)
        self.listSocket.append(udpServer)# 加入监听
        print('Add Corner:({name}:{langue}:{host},{port})'.format(name = name,langue = langue,host = self.localIP , port = udpPort))
        message = {}
        message['Head'] = 'CORNERSLIST'
        message['Data'] = self.corners
        JsonData = json.dumps(message).encode('utf-8')
        for user in self.userList:
            # JsonData = json.dumps(self.corners).encode('utf-8')
            user[1].sendall(JsonData)
        return corner

    def userEixt(self,addr):
        for user in self.userList:
            if addr == user[0]:
                self.listSocket.remove(user[1])
                self.userList.remove(user)
                message = {}
                message['Head'] = 'EXIT SERVER'
                message['Data'] = self.corners
                JsonData = json.dumps(message).encode('utf-8')
                user[1].sendall(JsonData)
                self.updateUserListUI()
                break

    def roomEixt(self,name):
        for corner in self.corners:
            if corner['name'] == name:
                # 通知所有用户
                sock = self.udpServer[self.corners.index(corner)]
                for user in corner['users']:
                    message = {}
                    message['From'] = ('System Message', '0')
                    message['To'] = 'all'
                    message['Data'] = 'Corner is closed!.'
                    JsonData = json.dumps(message).encode('utf-8')
                    sock.sendto(JsonData, user)

                self.corners.remove(corner)
                # 通知所有客户端
                message = {}
                message['Head'] = 'CORNERSLIST'
                message['Data'] = self.corners
                JsonData = json.dumps(message).encode('utf-8')
                for user in self.userList:
                    user[1].sendall(JsonData)
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
        self.server = Server(self.ui_Window)
        if self.server.status:
            self.ui_Window.label_6.setText('On Listen')
            self.ui_Window.label_7.setText(self.server.localIP)
            self.ui_Window.label_8.setText(str(self.server.serverPort))
        else:
            self.ui_Window.label_6.setText('Open Error')

    def closeEvent(self, *args, **kwargs):
        self.server.close()

    def NewCorner(self):
        name = self.ui_Window.lineEdit.text()
        langue = self.ui_Window.lineEdit_2.text()
        corner = self.server.openCorner(name,langue)
        self.server.updateCornerListUI()
        # if  corner!= {}:
        #     title = '{:<10s}(Langue:{:<10s}, Port:{:<5d})'.format(corner['name'],corner['langue'],corner['port'])
        #     self.ui_Window.listWidget_2.addItem(title)
        #     # self.ui_Window.listWidget_2
        pass

    def userForceExit(self,item):
        user = item.text()
        reply = QMessageBox.question(self, '提示',
                                     'Are you sure to Force Exit {0}?'.format(user),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            addr = (user.split(':')[0],int(user.split(':')[1]))
            self.server.userEixt(addr)
        else:
            pass

    def cornerClose(self,item):
        corner = item.text()
        reply = QMessageBox.question(self, '提示',
                                     'Are you sure to Destory {0}?'.format(corner),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            name = corner.split(' ')[0].strip()
            self.server.roomEixt(name)
        else:
            pass

if __name__ =='__main__':
    app = QApplication(sys.argv)
    mainWindow = ServerWindowDlg()
    mainWindow.show()
    sys.exit(app.exec_())
