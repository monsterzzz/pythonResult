import socket,select
import json,traceback
import threading
import time

class Message:
    def __init__(self,header,msg,rid=None,user=None):
        self.header = header
        self.msg = msg
        self.rid = rid
        self.user = user
    
    def to_json(self):
        return json.dumps({"header":self.header,"msg":self.msg,"rid":self.rid,"user":self.user})


    def __str__(self):
        return "{}  {}  {}".format(self.header,self.msg,self.rid)

class User:
    def __init__(self,id,name,password,current_addr = None):
        self.id = id
        self.name = name
        self.password = password
        self.current_addr = current_addr

class Room:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.user_conn = []

    def borad(self,msg,is_all = True,current_conn = None):
        err_conn = []
        if is_all:
            for i in self.user_conn:
                try:
                    i.send(bytes(msg,encoding="utf-8"))
                except:
                    err_conn.append(i)
                    
        else:
            for i in self.user_conn:
                if i != current_conn:
                    try:
                        i.send(bytes(msg,encoding="utf-8"))
                    except:
                        err_conn.append(i)
        for i in err_conn:
            self.user_conn.remove(i)


class Server:
    def __init__(self,port=9999):
        self.host = socket.gethostname()
        self.port = port
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        
    
    def run(self):
        self.s.bind((self.host,self.port))
        self.s.listen(10)
        connection_list = []
        connection_list.append(self.s)
        while True:
            rs,ws,es = select.select(connection_list,[],[])
            for i in rs:
                if i == self.s:
                    conn,addr = i.accept()
                    connection_list.append(conn)
                else:
                    try:
                        conn = i
                        data = conn.recv(1024)
                        if data:
                            threading.Thread(target = self.message_worker,args=(conn,data)).start()
                    except:
                        connection_list.remove(conn)
                        for i in chat_room:
                            if conn in i.user_conn:
                                i.borad(Message("exitRoom","other",i.id).to_json(),False,conn)

    def message_worker(self,conn,msg):
        msg = msg.decode("utf-8")
        try:
            msg = json.loads(msg)
            msg = Message(**msg)
        except:
            #import traceback
            #traceback.print_exc()
            pass
        print(msg)
        if msg == "hello":
            self.send(conn,Message("login","1").to_json())
        elif msg.header == "login":
            name,password = msg.msg.split("\n")
            flag = False
            for i in user:
                if i.name == name and i.password == password:
                    self.send(conn,Message("login","2").to_json())
                    flag = True
                    tmp = {}
                    tmp[name] = conn
                    current_user.append(tmp)
                    break
            if not flag:
                self.send(conn,Message("login","1").to_json())

        elif msg.header == "getRoom":
            self.send(conn,Message("roomList",[i.name for i in chat_room]).to_json())
        elif msg.header == "goRoom":
            for i in chat_room:
                if i.id == int(msg.msg):
                    i.user_conn.append(conn)
                    i.borad(Message("goRoom","1",msg.msg,msg.user).to_json())
                    break
        elif msg.header == "exitRoom":
            for i in chat_room:
                if i.id == int(msg.rid):
                    i.user_conn.remove(conn)
                    i.borad(Message("exitRoom","other",i.id).to_json(),True,conn)
                    self.send(conn,Message("exitRoom","self").to_json())
                    break
        elif msg.header == "chat":
            print("ddsssss")
            error_conn = []
            with open("chat_data.txt","a+",encoding="utf-8") as f:
                tmp = json.loads(msg.to_json())
                tmp['time'] = time.time() * 1000
                f.write(json.dumps(tmp) + "\n")
            for i in chat_room:
                if i.id == int(msg.rid):
                    i.borad(Message("chat","\n{} :\n{}\n".format(msg.user,msg.msg),msg.rid,msg.user).to_json(),False,conn)
                    break


    def send(self,conn,msg):
        conn.send(bytes(msg,encoding="utf-8"))
        



if __name__ == '__main__':
    with open("user.txt",'r',encoding="utf-8") as f:
        data = f.read()
    db_user = data.strip().split("\n")
    db_ul = [i.strip().split() for i in db_user]
    user = [User(int(i[0]),i[1],i[2]) for i in db_ul]
    chat_room = [Room(i,"room"+str(i)) for i in range(3)]
    current_user = []
    Server().run()