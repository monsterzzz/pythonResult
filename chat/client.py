import select,socket,sys
import threading,json
import pyaudio
import wave


class Message:
    def __init__(self,header,msg,rid=None,user=None):
        self.header = header
        self.msg = msg
        self.rid = rid
        self.user = user
    
    def to_json(self):
        return json.dumps({"header":self.header,"msg":self.msg,'rid':self.rid,"user":self.user})


    def __str__(self):
        return "{}  {}  {}".format(self.header,self.msg,self.rid)


class Client:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 9999
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        try:
            self.s.connect((self.host,self.port))
            print("connect success!")
        except:
            import traceback
            traceback.print_exc()
            print("connect server error!")


    def login(self):
        name = input("your name:")
        password = input("your password:")
        msg = Message("login","{}\n{}".format(name,password)).to_json()
        return msg

    def get_msg(self):
        connection_list = [self.s]
        while True:
            rs,ws,es = select.select(connection_list,[],[])
            for i in rs:
                if i == self.s:
                    try:
                        data = self.s.recv(1024)
                        print("!",data)
                        threading.Thread(target = self.message_worker,args = (data,)).start()
                    except:
                        print("connect stop...")
                        sys.exit()

    def message_worker(self,msg):
        msg = msg.decode("utf-8")
        try:
            msg = json.loads(msg)
            msg = Message(**msg)
        except:
            import traceback
            traceback.print_exc()
        print("str_msg",msg)
        if msg.header == "login":
            if msg.msg == "1":
                print("please login!")
                name = input("name:")
                password = input("password:")
                self.user = name
                self.send(Message("login","{}\n{}".format(name,password)).to_json())
            else:
                self.send(Message("getRoom","1").to_json())
        elif msg.header == "roomList":
            print("welcome to chatroom,please choose a room to go!")
            for i,v in enumerate(msg.msg):
                print("** {:<3}{:5} **".format(i,v))
            rid = input("choose a room: ")
            self.send(Message("goRoom",rid,rid,self.user).to_json())
        elif msg.header == "goRoom":
            if msg.msg == "1":
                print("{} go room {} success".format(msg.user,msg.rid))
                self.rid = msg.rid
                threading.Thread(target = self.play,args = ("up.wav",)).start()
                if msg.user == self.user:
                    threading.Thread(target = self.chat_ipt).start()
        elif msg.header == "chat":
            print(msg.msg)
        elif msg.header == "exitRoom":
            self.play("11.wav")
            if msg.msg == "self":
                print("goodbye~")
                self.s.close()
                sys.exit()
    
    def chat_ipt(self):
        while True:
            msg = input("")
            print("")
            if msg == "exit":
                self.send(Message("exitRoom",msg,self.rid,self.user).to_json())
                break
            else:
                self.send(Message("chat",msg,self.rid,self.user).to_json())


    def play(self,filename):
        wf = wave.open(filename, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while data != b'':
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()

        p.terminate()               

        
        
    def msg_input(self,):
        line = input('')
        return line.strip()

    def send(self,msg):
        self.s.send(bytes(msg,encoding="utf-8"))

    

client = Client()
threading.Thread(target=client.get_msg,).start()   # ①
# login 
client.send("hello")

    
    
