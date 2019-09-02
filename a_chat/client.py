import tkinter as tk
import threading
import socket

class Client:
    def __init__(self):
        self.server = Server()
        self.ui_root,ui_entry,ui_lb = self.setup_ui()
        threading.Thread(target = lambda : self.server.listen(ui_lb)).start()
        self.ui_root.mainloop()

    def setup_ui(self,title = "客户端",size = "600x400"):
        root = tk.Tk()
        root.geometry(size)
        root.title(title)

        lb=tk.Listbox(root,font=('',10))        
 
        lb.place(x=35,y=10,relwidth=0.9,relheight=0.85)
        
        #创建Scrollbar
        yscrollbar = tk.Scrollbar(lb,command=lb.yview)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lb.config(yscrollcommand=yscrollbar.set)

        entry = tk.Entry(root,width = 60)
        entry.place(x=35,y=360)
        root.protocol("WM_DELETE_WINDOW", self.close_window)
        bt = tk.Button(root,text = "click",command = lambda : self.server.send_msg(lb,entry))
        bt.place(x=480,y=360)
        return root,entry,lb

    def close_window(self):
        self.server.close()
        self.ui_root.destroy()


class Server:
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        port = 9090
        self.s.connect(("localhost",port))

    def send_msg(self,lb,et):
        msg = bytes(et.get(),"utf-8")
        threading.Thread(target = lambda : self.s.sendall(msg)).start()
        lb.insert("end", "[you]  : " + et.get())
        
        et.delete(0,"end")

    
    def listen(self,lb):
        while True:
            try:
                data = self.s.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
                lb.insert("end","[server]  :  "+str(data,"utf-8"))
                lb.see("end")
            except:
                break
        

    def close(self):
        self.s.close()    



Client()