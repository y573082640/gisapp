import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from AppMainWindow import appMainWindow  # 主窗体
from loginMainWindow import LoginMainWindow

app = QApplication(sys.argv)
main_form = LoginMainWindow()  # 主窗体

# 主窗体
main_form.show()
sys.exit(app.exec_())
