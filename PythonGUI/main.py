# coding=gbk
import os
import time
import sys
import Global_Var as globalvar
import cgitb
cgitb.enable( format = 'text')
from cv2 import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import time
import pygame
from Video_1 import Video1
from FaceAPI import Video2

pygame.init()

Ui_MainWindow, QtBaseClass_1 = uic.loadUiType("./GUI/MainWindow.ui")


globalvar._init()



class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)

        self.QUIT.clicked.connect(self.closeWindow)
        self.START.clicked.connect(self.STARTGAME)

        self.Sad.clicked.connect(lambda: self.answer('Sad'))
        self.Neutral.clicked.connect(lambda: self.answer('Neutral'))
        self.Disgust.clicked.connect(lambda: self.answer('Disgust'))
        self.Anger.clicked.connect(lambda: self.answer('Anger'))
        self.Surprise.clicked.connect(lambda: self.answer('Surprise'))
        self.Fear.clicked.connect(lambda: self.answer('Fear'))
        self.Happiness.clicked.connect(lambda: self.answer('Happiness'))


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(50)


        self.Vision_1_Thread = Vision_1_Thread()
        # Face_Thread
        self.Face_Thread = Face_Thread()
        self.Face_Thread.FinishSignal.connect(self.FinsihProcess)


        self.SettingConfig()


    def operate(self):
        if globalvar.Get_value('time_count') == None:
            temp_image = globalvar.Get_value('temp_image')
            if temp_image:
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.showpic(temp_pixmap)
            globalvar.Set_value('face', None)

 
        else:

            Position = self.label_4.geometry()
            pixmap = QPixmap('./Files/rainbow.png').scaled(Position.width(),
                                                           Position.height())

            p = QPainter(pixmap)
            p.begin(pixmap)
            p.fillRect(0, 0, int(Position.width()),
                       int(Position.height()- 65.4 * (globalvar.Get_value('Score')-1) - globalvar.Get_value('time_count')/40* 65.4 ),
                       QColor(255, 255, 255, 255))
            self.label_4.setPixmap(pixmap)
            p.end()

            globalvar.Set_value('time_count', globalvar.Get_value('time_count') + 1)

            if globalvar.Get_value('time_count') >= 40:
                globalvar.Set_value('time_count', None)
                self.movie.stop()
                self.label_15.setText(' ')
                self.label_13.setText(' ')
                self.label_14.setText(' ')
                if globalvar.Get_value('Score') == 10:
                    self.timer.stop()
                    self.OpenWarningBox('Congrats，you gain 10 score~')




    def showpic(self, png):
        Position = self.label.geometry()
        scaredPixmap = png.scaled(Position.width() ,
                                  Position.height())
        self.label.setPixmap(scaredPixmap)


    def closeWindow(self):
        self.close()


    def closeEvent(self, event):
        globalvar.Set_value('Exit_Flag', True)
        time.sleep(0.3)
        event.accept()

    
    def OpenWarningBox(self, Messages_S):
        box = QtWidgets.QMessageBox()
        Messages_S = Messages_S
        box.warning(self, 'Warning', Messages_S, box.Ok)

    
    def SettingConfig(self):
        globalvar.Set_value('Exit_Flag', False)
        self.Vision_1_Thread.start()
        self.label_12.setText('Current Score：')


    def STARTGAME(self):
        self.label_12.setText('Current Score：')
        self.label_15.setText(' ')
        self.label_13.setText(' ')
        self.label_14.setText(' ')
        self.label_4.setText(' ')
        globalvar.Set_value('Score', 0)
        self.timer.start(50)


    def answer(self,FACE):
        if globalvar.Get_value('face'):
            if globalvar.Get_value('Score')== None:
                globalvar.Set_value('Score', 0)
            if FACE == globalvar.Get_value('face'):
                png = QPixmap('./Files/checkmark.png')
                self.label_13.setText('Correct！')
                self.label_12.setText('Current Score：' + str(globalvar.Get_value('Score') + 1))
                globalvar.Set_value('Score', globalvar.Get_value('Score') + 1)

                if globalvar.Get_value('Score') >10:
                    globalvar.Set_value('Score', 10)
                    self.OpenWarningBox('Congrats! You did it!')
                else:
                    self.timer.start(50)
                    globalvar.Set_value('time_count', 0)
                    self.showpic(QPixmap('./Files/Next.png'))
   
                    self.movie = QtGui.QMovie("./Files/firework1.gif")
        
                    self.movie.setCacheMode(QtGui.QMovie.CacheAll)
             
                    self.movie.setSpeed(100)
                    
                    self.label_15.setMovie(self.movie)
                 
                    self.movie.start()
                    sound = pygame.mixer.Sound(r"./Files/correct2.wav")
                    sound.set_volume(1)
                    sound.play()

            else:
                png = QPixmap('./Files/wrongcross.png')
                self.label_13.setText('Try Again~')
                sound = pygame.mixer.Sound(r"./Files/wrong.wav")
                sound.set_volume(1)
                sound.play()

            Position = self.label_14.geometry()
            scaredPixmap = png.scaled(Position.width(),
                                      Position.height())
            self.label_14.setPixmap(scaredPixmap)



    def FinsihProcess(self, req_dict):
        print(req_dict)
        # self.OpenWarningBox(str(req_dict[1]))
        globalvar.Set_value('face', str(req_dict[1]))
        # self.timer.start(50)
        temp_image = self.temp_image
        if temp_image:
            temp_pixmap = QPixmap.fromImage(temp_image)
            self.showpic(temp_pixmap)


    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        # if event.button()==QtCore.Qt.RightButton:
        #     self.hide()

    def mouseDoubleClickEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
         
            x = event.pos().x()
            y = event.pos().y()
            if globalvar.Get_value('Score') == 10:
                self.OpenWarningBox('Congrats，you gain 10 score~')
            else:
                if x > 134 and x < 737 and y > 101 and y < 504:
                    self.timer.stop()
            
                    self.temp_image = globalvar.Get_value('temp_image')
                    self.temp_image.save("cache.png")
                    self.Face_Thread.start()
                    png = QPixmap('./Files/wait.png')
                    self.showpic(png)

    def mouseMoveEvent(self,event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()




class Vision_1_Thread(QThread):
  
    timeSignal = pyqtSignal()
    def __init__(self, parent=None):
        super(Vision_1_Thread, self).__init__(parent)

    def run(self):
        v1 = Video1()
        v1.run()


class Face_Thread(QThread):

    FinishSignal = pyqtSignal(list)
    def __init__(self, parent=None):
        super(Face_Thread, self).__init__(parent)

    def run(self):
        v2 = Video2()
        req_dict,result_str = v2.run()
        self.FinishSignal.emit([req_dict,result_str])




if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


