# -*- coding : utf-8 -*-
# @Author : Dynamt
# @Time: 2023-01-09 19:39
# 名称 ： 简易视频播放器
# 功能实现 ：本地视频列表播放，切换等
"""
注：需要安装视频解码器才能顺利播放视频，直接安装本目录下的LAVFilters-0.75.1-Installer.exe文件
或下载地址：https://www.videohelp.com/download/LAVFilters-0.75.1-Installer.exe
"""

import sys,os
from PyQt5.QtWidgets import QApplication,QFileDialog,QMainWindow
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from Ui_VideoPlayer import Ui_VideoPlayer
from PyQt5.QtGui import QCursor


class VideoPlayerMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.ui.wgt_videoplayer)
        self.loop=0

        # 按钮和文件夹打开槽函数连接信号
        self.ui.btn_play.clicked.connect(self.play)
        self.ui.btn_file.clicked.connect(self.openfile)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_pause.clicked.connect(self.pause)
        self.ui.btn_pre.clicked.connect(self.preVideo)

        # 进度条
        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.ui.horizontalSlider.sliderMoved.connect(self.updatePosition)

    def init_list(self,vlist:list[str]=None):
        """
        初始化播放列表
        :param vlist: 若为None,则说明是在播放器中打开的播放列表,self.video已初始化完毕,只需放入播放列表中即可
                      若为一个列表,说明列表只有视频文件的绝对路径,不能直接用
        :return:
        """
        try:
            if vlist == None:
                mediaContent = QMediaContent(QUrl(self.video[self.loop]))
                self.player.setMedia(mediaContent)
            else:
                if vlist==[] or vlist==['']:
                    return
                self.video=[]
                for v in vlist:  # 完整路径,但是没有file:///
                    v = 'file:///' + v  # TODO:注意要加file:///
                    self.video.append(v)
            mediaContent = QMediaContent(QUrl(self.video[self.loop]))
            self.player.setMedia(mediaContent)
        except:
            print("初始化视频列表错误")
            return

    def displayName(self):
        name = self.video[self.loop].split('/')[-1]
        self.ui.label_name.setText(name)

    def play(self):
        try:
            self.player.play()
            self.displayName()
        except:
            return

    def openfile(self):
        self.video = []
        fdir = QFileDialog.getExistingDirectory(None, "请选择文件夹路径")
        print(fdir)
        for root, dirs, files in os.walk(fdir):
            for file in files:
                # 使用join函数将文件名称和文件所在根目录连接起来
                file = os.path.join(root, file)
                file = 'file:///'+file   # TODO:注意要加file:///
                self.video.append(file)
        self.init_list()


        # 同样的方式，更直接的形式，但是得不到播放列表
        # fileUrl = QFileDialog.getOpenFileUrl()[0]
        # PyQt5.QtCore.QUrl('file:///D:/Huawei Share/Screenshot/20220907_134347.mp4')
        # mediaContent = QMediaContent(fileUrl)
        # self.player.setMedia(mediaContent)
        # print(type(fileUrl))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def next(self):
        try:
            self.loop += 1
            self.loop = self.loop % len(self.video)
            mediaContent = QMediaContent(QUrl(self.video[self.loop]))
            self.player.setMedia(mediaContent)
            self.play()
        except:
            return

    def preVideo(self):
        try:
            self.loop -= 1
            self.loop = self.loop % len(self.video)
            mediaContent = QMediaContent(QUrl(self.video[self.loop]))
            self.player.setMedia(mediaContent)
            self.play()
        except:
            return

    def pause(self):
        try:
            self.player.pause()
        except:
            return

    def getDuration(self,d):
        """获取视频总时长，d"""
        self.ui.horizontalSlider.setRange(0,d)
        self.ui.horizontalSlider.setEnabled(True)
        self.displayTime(d)

    def getPosition(self,p):
        self.ui.horizontalSlider.setValue(p)
        self.displayTime(self.ui.horizontalSlider.maximum()-p)

    def displayTime(self,ms):
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.ui.timeDisplay.setText(f'{minutes}:{seconds}')

    def updatePosition(self,v):
        try:
            self.player.setPosition(v)
            self.displayTime(self.ui.horizontalSlider.maximum()-v)
        except:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player_form = VideoPlayerMainWindow()

    player_form.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框
    # player_form.setAttribute(Qt.WA_TranslucentBackground)
    player_form.setWindowOpacity(0.95)

    player_form.show()
    sys.exit(app.exec_())