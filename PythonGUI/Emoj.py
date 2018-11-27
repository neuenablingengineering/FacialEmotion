#!Anaconda/anaconda/python
#coding: utf-8
# import dlib
# import numpy as np
import cv2
import Global_Var as globalvar
from PyQt5.QtGui import *
class face_emotion():

    def __init__(self):

       
        self.cap = cv2.VideoCapture(0)
        
        self.cap.set(3, 480)
        
        self.cnt = 0

    def learning_face(self):

        while(self.cap.isOpened()):

            
            flag, im_rd = self.cap.read()

         
            k = cv2.waitKey(1)

          
            font = cv2.FONT_HERSHEY_SIMPLEX

            
            im_rd = cv2.putText(im_rd, "Click Shot Screen", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            # im_rd = cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
            temp_pixmap = QPixmap.fromImage(temp_image)
            globalvar.Set_value('temp_pixmap', temp_pixmap)

  
            if(globalvar.Get_value('Exit_Flag') == True):
                break

    
            # cv2.imshow("Camera", im_rd)

        self.cap.release()


        cv2.destroyAllWindows()


if __name__ == "__main__":
    my_face = face_emotion()
    my_face.learning_face()

