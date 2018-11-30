# import the necessary packages
import cv2
import picamera
import Global_Var as globalvar
from PyQt5.QtGui import *
import imutils
import numpy as np

class Video1:

    def run(self):
        self.cap = cv2.VideoCapture(1)

        while (self.cap.isOpened()):

            ret, frame = self.cap.read()


            font = cv2.FONT_HERSHEY_SIMPLEX


            cv2.putText(frame, "Double Click to Take Picture", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            height, width = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # globalvar.Set_value('frame', frame)
            temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
            globalvar.Set_value('temp_image', temp_image)
            # temp_pixmap = QPixmap.fromImage(temp_image)
            # globalvar.Set_value('temp_pixmap', temp_pixmap)

            
            if (globalvar.Get_value('Exit_Flag') == True):
                break


        self.cap.release()
