


import tkinter as tk
import threading
import socket

class BackServer:
    def __init__(self):
        self.server = Server()
        self.ui_root,ui_lb = self.setup_ui()
        threading.Thread(target = lambda : self.server.listen(ui_lb)).start()
        self.ui_root.mainloop()

    def setup_ui(self,title = "服务器",size = "600x400"):
        root = tk.Tk()
        root.geometry(size)
        root.title(title)

        lb=tk.Listbox(root,font=('',14))        
 
        lb.place(x=35,y=10,relwidth=0.9,relheight=0.9)
        
        #创建Scrollbar
        yscrollbar = tk.Scrollbar(lb,command=lb.yview)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lb.config(yscrollcommand=yscrollbar.set)

        # entry = tk.Entry(root,width = 60)
        # entry.place(x=35,y=360)
        root.protocol("WM_DELETE_WINDOW", self.close_window)
        # bt = tk.Button(root,text = "click",command = lambda : self.server.send_msg(lb,entry))
        # bt.place(x=480,y=360)
        return root,lb

    def close_window(self):
        self.server.close()
        self.ui_root.destroy()


class Server:
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(("localhost",9090))
        self.s.listen(5) #开始监听 表示可以使用五个链接排队

    def listen(self,lb):
        while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
            try:
                conn,addr = self.s.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
                if conn:
                    threading.Thread(target = self.t_client,args = (conn,addr,lb,)).start()
            except Exception as e:
                import traceback
                traceback.print_exc()
                break
                
    def t_client(self,conn,addr,lb):
        while True:
            try:
                data = conn.recv(1024)  #接收数据
                if data :
                    lb.insert("end","[{}:{}] : {}".format(*addr,str(data,"utf-8")))
                    lb.see("end")
                    conn.send(bytes("hi~" + str(data,"utf-8"),"utf-8")) #然后再发送数据
            except:
                break
        conn.close()

    def close(self):
        
        self.s.close()    



BackServer()