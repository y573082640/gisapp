# -*- coding : utf-8 -*-
# @Author : Dynamt
# @Time: 2023-01-09 18:53
# 名称 ： 简易音频播放器
# 功能实现 ：本地音频列表播放，切换等

import sys,time,pygame,os
from PyQt5.QtWidgets import QWidget,QApplication,QFileDialog,QMessageBox,QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from Ui_MusicPlayer import Ui_MusicPlayer


class MusicPlayerMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MusicPlayer()
        self.ui.setupUi(self)

        self.music =[]  # 测试  ['D:\CloudMusic\download_music\手写的从前 - 周杰伦.mp3','D:\CloudMusic\download_music\明明就 - 周杰伦.mp3']
        self.loop = 0
        self.pause_flag = False

        self.ui.btn_play.clicked.connect(self.play)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_pause.clicked.connect(self.pause)
        self.ui.btn_file.clicked.connect(self.get_music)
        self.ui.btn_pre.clicked.connect(self.pre)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)

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


    def play(self):
        try:
            print(self.music[self.loop])
            if self.pause_flag == True:
                pygame.mixer.music.pause()
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
        except:
            return

    def next(self):
        try:
            pygame.mixer.music.stop()
            self.loop +=1
            self.loop=self.loop % len(self.music)

            self.track = pygame.mixer.music.load(str(self.music[self.loop]))
            name = self.music[self.loop].split('/')[-1]
            self.ui.textBrowser.setText(name)
            pygame.mixer.music.play()
        except:
            return

    def pre(self):
        try:
            pygame.mixer.music.stop()
            self.loop -= 1
            self.loop=self.loop % len(self.music)
            # print(self.loop)

            self.track = pygame.mixer.music.load(str(self.music[self.loop]))
            name = self.music[self.loop].split('/')[-1]
            self.ui.textBrowser.setText(name)
            pygame.mixer.music.play()
        except:
            return

    def pause(self):
        try:
            pygame.mixer.music.pause()
            self.pause_flag = True
        except:
            return

    def get_music(self):
        self.music=[]
        fdir = QFileDialog.getExistingDirectory(None,"请选择文件夹路径")
        print(fdir)
        for root, dirs, files in os.walk(fdir):
            for file in files:
                # 使用join函数将文件名称和文件所在根目录连接起来
                file = os.path.join(root, file)
                self.music.append(file)
        print(self.music)

    def init_list(self,fp:list):
        try:
            # if fp==[] or fp ==['']:
            #     return
            self.music=fp
            pygame.init()
            self.track = pygame.mixer.music.load(str(self.music[self.loop]))
            name = self.music[self.loop].split('/')[-1]
            self.ui.textBrowser.setText(name)
        except:
            return


if __name__=="__main__":
    app = QApplication(sys.argv)
    player_form = MusicPlayerMainWindow()

    player_form.show()
    sys.exit(app.exec_())