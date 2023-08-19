import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QMessageBox
from Ui_login import Ui_MainWindow
from PyQt5.QtCore import Qt
import pandas as pd
import json
import datetime
from AppMainWindow import appMainWindow  # 主窗体

# 使用一个本地csv储存用户信息
class LoginMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.signin)
        self.ui.pushButton_2.clicked.connect(self.register)
        # csv文件路径，需要修改为最后使用时的文件地址
        # TODO
        self.path = './userData/users.csv'
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏框
        self.setAttribute(Qt.WA_TranslucentBackground)

    # 将DF写入csv文件（更新用户数据）
    def WriteInCSV(self):
        self.DF.to_csv(self.path, index=False)
    # 读出用户信息
    def ReadCSV(self):
        self.DF = pd.read_csv(self.path)

    # 注册信息
    def register(self):
        self.ReadCSV()
        name = self.ui.lineEdit_5.text()
        names = self.DF['names'].tolist()
        flag = False #标注是否有重复用户名
        for i in names:
            if name == i:
                flag = True
        if flag == False:
            pin1 = str(self.ui.lineEdit_4.text())
            pin2 = str(self.ui.lineEdit_6.text())
            if pin1 == pin2:
                N = len(self.DF.index)
                self.DF.loc[N] = [name, pin1]
                self.WriteInCSV()
                QMessageBox.information(None, '注册', '注册成功，请转至登录页面登录', QMessageBox.Ok)
                self.code = pin1
                self.NewUser(name, N+1)
            else:
                QMessageBox.warning(None, '警告', '输入密码不一致!', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '该用户名已存在', QMessageBox.Ok)

    def signin(self):
        self.ReadCSV()
        name = self.ui.lineEdit_2.text()
        pin = str(self.ui.lineEdit_3.text())
        names = self.DF['names'].tolist()
        flag_n = False
        flag_p = False
        for i in names:
            if name == i:
                flag_n = True
                ip = str(self.DF[self.DF.names == name].iloc[0, 1])
                if ip == pin:
                    flag_p = True
        if flag_p:
            self.Switch(name)
            self.close()
            # QMessageBox.information(None, '登录', '登录成功', QMessageBox.Ok)
            self.MW = appMainWindow()
            self.MW.setUser(name)
            self.MW.show()
        elif flag_n:
            QMessageBox.warning(None, '警告', '密码错误', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '未查询到该用户，请先注册！', QMessageBox.Ok)

    def NewUser(self, NAME:str, N):
        code = str(datetime.date.today()) + '-' + str(N)
        # 最初的用户文件包括用户信息和一个已标记的点数据，为北师大
        dict_user = {'user_ID': N, 'user_name': NAME, 'user_code': self.code, 'points': {"\u5317\u4eac\u5e08\u8303\u5927\u5b66": {"state": 1, "place": "\u5317\u4eac\u5e08\u8303\u5927\u5b66", "locationXY": {"X": 116.364139, "Y": 39.962637}, "time": [2022, 12, 28], "date": 20221228, "text": "None", "p": [], "m": [], "v": []}}}
        json.dump(dict_user, open(f'./userData/user.{NAME}.json', 'w'), indent=4)

    def Switch(self, NAME:str):
        self.userjson = f'./userData/user.{NAME}.json'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_form = LoginMainWindow()
    login_form.show()
    sys.exit(app.exec_())