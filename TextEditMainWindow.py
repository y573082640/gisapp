# -*- coding : utf-8 -*-
# @Author : Dynamt
# @Time: 2023-01-10 22:51
# 名称 ： TextEditMainWindow.py
# 功能实现 ：文本编辑

import sys,time,pygame,os
from PyQt5.QtWidgets import QWidget,QApplication,QFileDialog,QMessageBox,QMainWindow,QColorDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt,QDate


from Ui_TextEdit import Ui_MainWindow


class TextEditMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)

        # 槽函数连接
        # self.ui.btn_save2.clicked.connect(self.save)
        self.ui.btn_save.clicked.connect(self.save) #保存
        self.ui.spinBox_fontsize.valueChanged.connect(self.fontSize)
        self.ui.btn_bold.clicked.connect(self.setBold)
        self.ui.btn_italy.clicked.connect(self.setItaly)
        self.ui.btn_color.clicked.connect(self.setColor)
        # self.ui.fontComboBox.currentIndexChanged.connect(self.setfont)
        self.ui.textEdit.selectionChanged.connect(self.selectChanged)
        self.ui.dateEdit.setDate(QDate.currentDate())

    def setHtmlTxt(self,txthtml):
        """
        设置展示的接口函数
        :param txthtml:
        :return:
        """
        self.ui.textEdit.setHtml(txthtml)

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

    def save(self):
        fname,_ = QFileDialog.getSaveFileName(self,"保存文字为html文件","(*.html)")
        if fname.split('.')[-1] != "html":
            print("没得到文件")
            # mes = QMessageBox.information(self,"保存","未保存！请选择正确保存路径。",QMessageBox.Ok)
            msg_box = QMessageBox(QMessageBox.Question, '保存', '未保存！请选择正确保存路径。')  # 退出表示弹出框标题，"你确定退出吗？"表示弹出框的内容
            msg_box.exec_()
            return
        print(fname)
        with open(fname,'w') as f:
            f.write(self.ui.textEdit.toHtml())





    def getHtml(self):
        html = self.ui.textEdit.toHtml()
        return html


    def fontSize(self):
        self.fsize=self.ui.spinBox_fontsize.value()
        self.ui.textEdit.setFontPointSize(float(self.fsize))

    def setBold(self):
        pass

    def setItaly(self):
        pass

    def setColor(self):
        color = QColorDialog.getColor(Qt.red,self,"选择字体颜色")
        if color.isValid():
            red,green,blue,_=color.getRgb()
            self.fsize=self.ui.spinBox_fontsize.value()
            # self.ui.textEdit.setTextColor()
            # self.ui.textEdit.setStyleSheet(f"color:rgb({red},{green},{blue});font-size:{self.fsize}px")#font-size:{self.fsize}px

    def selectChanged(self):
        fontsize = self.ui.textEdit.currentCharFormat()


if __name__=="__main__":
    app = QApplication(sys.argv)
    editor_form = TextEditMainWindow()

    editor_form.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框
    editor_form.setAttribute(Qt.WA_TranslucentBackground)
    editor_form.setWindowOpacity(0.95)


    editor_form.show()
    sys.exit(app.exec_())