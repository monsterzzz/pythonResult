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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget, QMessageBox,QTableWidgetItem
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
    def __init__(self):
        super().__init__()
        self.ui_Window = Ui_watch()
        self.ui_Window.setupUi(self)
        self.Qipan = Qipan(self)
        #self.father_frame = father
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

    


if __name__ =='__main__':
    app = QApplication(sys.argv)
    main_window = WatchUI()
    main_window.show()
    sys.exit(app.exec_())