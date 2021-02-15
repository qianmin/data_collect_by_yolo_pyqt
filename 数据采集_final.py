#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2
import time
import cv2
import torch


from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
# from yolo_base.pyqt_yolov5_picture import yolov5
from base_pack.file_class import yolo_file
from base_pack.yolo_base.pyqt_yolov5_picture import yolov5

font = QtGui.QFont()
font.setFamily("Arial") #括号里可以设置成自己想要的其它字体
font.setPointSize(18)   #括号里的数字可以设置成自己想要的字体大小

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0

        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.img = 0
        self.tmp_img=0
        self.result_img=0

        self.set_ui()
        self.slot_init()

        ###yolo
        self.model=0
        self.result_all = 0
        self.result_one = 0
        ###yolo

        ###file_class
        self.file_process=0
        ###file_class

    def set_ui(self):
        # 混合布局
        self.w_layput = QVBoxLayout()
        self.source_layout = QHBoxLayout()
        self.input_layout = QHBoxLayout()
        self.process_layout=QHBoxLayout()
        self.btn_layout=QHBoxLayout()



        # source_layout 全部
        self.btn_init=QPushButton(u'1:初始化yolov5、相机功能')
        self.btn_init.setStyleSheet("background-color:rgb(255,0,0)")
        self.btn_init.setMaximumSize(400,50)
        self.btn_init.setFont(font)
        self.label_source = QLabel()
        self.label_source.setFixedSize(640, 480)
        self.source_layout.addWidget(self.label_source)
        self.source_layout.addWidget(self.btn_init)

        #input_layout全部
        self.label_input = QLabel()
        self.label_input.setText('输入保存文件夹')
        self.label_input.setFont(font)
        self.label_input.setFixedSize(300, 50)

        self.line_dir = QLineEdit()
        self.line_dir.setFont(font)
        self.line_dir.setText('./data/people/')
        self.line_dir.setFixedSize(500, 50)

        self.btn_init_save=QPushButton()
        self.btn_init_save.setText('2:初始化文件保存功能')
        self.btn_init_save.setStyleSheet("background-color:rgb(255,0,0)")
        self.btn_init_save.setMaximumSize(400,50)
        self.btn_init_save.setFont(font)
        # self.btn_init_save.setFixedSize(200,50)


        self.input_layout.addWidget(self.label_input)
        self.input_layout.addWidget(self.line_dir)
        self.input_layout.addWidget(self.btn_init_save)

        #process_layout全部
        self.label_one_img = QLabel()
        self.label_one_img.setFixedSize(640, 480)
        self.label_result_all = QLabel()
        self.label_result_all.setFixedSize(640, 480)
        self.label_result_one = QLabel()
        self.label_result_one.setFixedSize(320, 240)

        self.process_layout.addWidget(self.label_one_img)
        self.process_layout.addWidget(self.label_result_all)
        self.process_layout.addWidget(self.label_result_one)

        #btn_layout全部
        self.btn_process_one=QPushButton(u'处理一帧')
        self.btn_process_one.setMinimumSize(400,100)
        self.btn_process_one.setMinimumSize(300,100)
        self.btn_process_one.setFont(font)
        self.btn_del_one=QPushButton(u'删除上一个保存结果')
        self.btn_del_one.setMinimumSize(400,100)
        self.btn_del_one.setMinimumSize(300,100)
        self.btn_del_one.setFont(font)

        self.btn_layout.addWidget(self.btn_process_one)
        self.btn_layout.addWidget(self.btn_del_one)

        # 初始化全部布局
        self.w_layput.addLayout(self.source_layout)
        self.w_layput.addLayout(self.input_layout)
        self.w_layput.addLayout(self.process_layout)
        self.w_layput.addLayout(self.btn_layout)

        self.setLayout(self.w_layput)
        self.setWindowTitle(u'摄像头')
        self.resize(1920,1080)

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)

        self.btn_init.clicked.connect(self.f_btn_init)

        self.btn_init_save.clicked.connect(self.f_btn_init_save)

        self.btn_process_one.clicked.connect(self.f_btn_process_one)

        self.btn_del_one.clicked.connect(self.f_btn_del_one)
        # self.btn_open_cam.clicked.connect(self.button_open_camera_click)
        # self.btn_get_one.clicked.connect(self.get_one_img)
        # self.btn_detect.clicked.connect(self.detect_one_img)
        # self.btn_save.clicked.connect(self.f_save)
        # self.btn_init_save.clicked.connect(self.init_file_save)


    '''
    一步一步的功能
    '''
    def init_file_save(self):
        save_path=self.line_dir.text()
        self.file_process=yolo_file(save_path)
        print(save_path)

    def button_open_camera_click(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
            # self.btn_open_cam.setText(u'关闭相机')
    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_source.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def get_one_img(self):
        self.tmp_img=self.image
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_one_img.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def f_save(self):
        self.file_process.save_one_img(self.result_one)

    def detect_one_img(self):
        self.result_all,self.result_one=self.model.detect(self.tmp_img)
        show1=self.result_all
        show2=self.result_one

        show1= cv2.resize(show1, (640, 480))
        show2 = cv2.resize(show2, (320, 240))
        show1 = cv2.cvtColor(show1, cv2.COLOR_BGR2RGB)
        show2 = cv2.cvtColor(show2,cv2.COLOR_BGR2RGB)
        showImage_all = QtGui.QImage(show1.data, show1.shape[1], show1.shape[0],
                                     QtGui.QImage.Format_RGB888)
        showImage_one = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)



        self.label_result_all.setPixmap(QtGui.QPixmap.fromImage(showImage_all))
        self.label_result_one.setPixmap(QtGui.QPixmap.fromImage(showImage_one))
    '''
    一步一步的功能
    '''



    def f_btn_init(self):
        #red 255,0,0  green 0,255,0
        self.btn_init.setStyleSheet("background-color:rgb(0,255,0)")
        self.button_open_camera_click()
        self.model = yolov5()

    def f_btn_init_save(self):
        self.init_file_save()
        self.btn_init_save.setStyleSheet("background-color:rgb(0,255,0)")

    def f_btn_process_one(self):
        self.get_one_img()
        self.detect_one_img()
        self.f_save()

    def f_btn_del_one(self):
        self.file_process.del_last_img()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())