import os,io
from Ui_AppMainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QCompleter,QMessageBox,QFileDialog,QDockWidget,QHBoxLayout,QPushButton,QTextBrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QUrl
import requests
import json

from PyQt5.QtCore import QTimer,QDate

from TextEditMainWindow import TextEditMainWindow
from MusicPlayerMainWindow import MusicPlayerMainWindow
from VideoPlayerMainWindow import VideoPlayerMainWindow
from Feature_Info import FeatureInfo
from RoutePlanning_algorithm import route_planning

import GeographicCoding
from InitMap_re import MyMap
from Mapbuilding import Map
import pandas as pd
import folium
from datetime import datetime


import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtNetwork import QNetworkProxyFactory
QNetworkProxyFactory.setUseSystemConfiguration(False)

class appMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_name = None

        # 子窗体的信号设置
        self.textEditor_form = TextEditMainWindow()
        self.musicPlayer_form = MusicPlayerMainWindow()
        self.videoPlayer_form = VideoPlayerMainWindow()
        self.ui.btn_playVideo.clicked.connect(self.videoPlayer_form_show)
        self.ui.btn_playMusic.clicked.connect(self.musicPlayer_form_show)
        self.ui.btn_editor.clicked.connect(self.textEditor_form.show)

        # dockWidget的隐藏和显示
        self.ui.dockWidget_feature.hide()
        self.ui.dockWidget_RouteGuide.hide()
        self.ui.actionfeatureInfo.triggered.connect(self.ui.dockWidget_feature.show)
        self.ui.actionRouteGuide.triggered.connect(self.ui.dockWidget_RouteGuide.show)
        self.ui.actionRouteGuide.triggered.connect(self.Change2Tab_folium)
        self.ui.actionopen_file.triggered.connect(self.Change2Tab_mapCanvas)

        # 路线规划
        self.ui.btn_routeGuide.clicked.connect(self.ui.dockWidget_RouteGuide.show)
        self.ui.btn_routeGuide.clicked.connect(self.Change2Tab_folium)
        self.ui.btn_routeGuide.clicked.connect(self.routeGuide_Init)
        self.ui.btn_routeGuide_bike.clicked.connect(self.routePlanning_bike)
        self.ui.btn_routeGuide_car.clicked.connect(self.routePlanning_car)
        self.ui.btn_routeGuide_bus.clicked.connect(self.routePlanning_bus)
        self.ui.btn_routeGuide_walk.clicked.connect(self.routePlanning_walk)
        self.ui.btn_changeDire.clicked.connect(self.change_direction)
        self.ui.dateEdit.setDate(QDate.currentDate())

        # 打开文件夹获取音视频和图片的路径
        self.ui.btn_addMusic.clicked.connect(self.addMusicPath)
        self.ui.btn_addVideo.clicked.connect(self.addVideoPath)
        self.ui.btn_addpicture.clicked.connect(self.addPicPath)

        self.ui.btn_editor.clicked.connect(self.getFeatureText2subMW)
        self.textEditor_form.ui.btn_save2.clicked.connect(self.saveFeatureText)

        # 展示图片
        self.picLoop = 0
        self.pictures =[]
        self.ui.btn_pre_pic.clicked.connect(self.pre_pic)
        self.ui.btn_next_pic.clicked.connect(self.next_pic)

        # 关于folium 与QtWebEngineView
        self.webview = self.ui.webEngineView
        self.data, self.m = self.InitMap_re()
        self.webview.setHtml(self.data.getvalue().decode())
        # 初始化底图
        self.webview = self.ui.webEngineView
        self.mapcenter = [40.182177, 116.437618]
        self.pointdata = pd.read_excel(r'.\景区信息\风景名胜.xls')
        geourl = 'https://a.amap.com/jsapi_demos/static/geojson/beijing.json'
        geostyle = lambda x: {'fillColor': '#0000ff', 'fillOpacity': 0.2, 'line_opacity': 0.2}
        self.zoom = 9
        self.map = MyMap(self.mapcenter, self.pointdata, geourl, geostyle, self.zoom)  # 底图对象
        #mmap = MyMap(self.mapcenter, self.pointdata, geourl, geostyle, self.zoom)  # 底图对象
        # 显示
        #self.webview.load(QUrl(mmap.get_mapurl()))  # 加载点 mmap.get_mapurl() 'https://zhuanlan.zhihu.com/p/361677024' "file:/D:/00A大三下课程资料/GIS开发期末大作业/App_final/test.html"
        #self.type = 0

        # 地图对象
        # self.m = mmap.m

        self.smart_search(self.pointdata['NAME'])

        self.walkingDepartureAddress = None  # 出发地址
        self.walkingDestinationAddress = None  # 终点地址

        # 查询槽函数连接
        self.place_now = None

        self.ui.btn_addPoint.clicked.connect(self.addPoint2UserData)
        self.ui.btn_update.clicked.connect(self.update_feature)
        #
        self.ui.searchButton.clicked.connect(self.showFeatures)
        # self.ui.startlineEdit.editingFinished.connect(self.getstartxy)
        # self.ui.searchButton.clicked.connect(self.showFeatures)


    def videoPlayer_form_show(self):
        if self.feat.getPath('v')==[]:
            QMessageBox.warning(None,"提示","未添加过视频,请先添加视频",QMessageBox.Ok)
        else:
            self.videoPlayer_form.show()

    def musicPlayer_form_show(self):
        if self.feat.getPath('m')==[]:
            QMessageBox.warning(None,"提示","未添加过视频,请先添加音乐",QMessageBox.Ok)
        else:
            self.musicPlayer_form.show()

    def setPlaceNow_dock(self):   # TODO：合并到update中
        self.place_now = self.ui.endlineEdit.text()
        print(self.place_now)
        self.ui.feat_name_D1.setText(self.place_now)

    def setUser(self,user_name):
        # 要素属性展示
        self.feat = FeatureInfo(user_ID=user_name)  # 测试,登录时初始化一个用户的json文件,用

    # 路线规划信息
    def routeGuide_Init(self):
        self.ui.feat_name_D2.setText(self.ui.feat_name_D1.text())
        self.ui.lineEdit_start.setText("北京师范大学")    # TODO:在这修改起始点
        self.ui.lineEdit_stop.setText(self.place_now)

    def change_direction(self):
        s = self.ui.lineEdit_start.text()
        self.ui.lineEdit_start.setText(self.ui.lineEdit_stop.text())
        self.ui.lineEdit_stop.setText(s)

    def routePlanning_bike(self):
        """
        出行方式（1.公交、2.步行、3.驾车、4.骑行）
        :return:
        """
        try:
            self.routePlaning(route_planning(self.ui.lineEdit_start.text(),self.ui.lineEdit_stop.text(),4))
            type = '4'
            self.route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), type)

        except:
            self.ui.route_text.setText("请选择其他出行方式")

    def routePlanning_bus(self):
        try:
            self.routePlaning(route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), 1))
            type = '1'
            self.route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), type)
        except:
            self.ui.route_text.setText("请选择其他出行方式")

    def routePlanning_car(self):
        try:
            self.routePlaning(route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), 3))
            type = '3'
            self.route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), type)
        except:
            self.ui.route_text.setText("请选择其他出行方式")

    def routePlanning_walk(self):
        try:
            self.routePlaning(route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), 2))
            type = '2'
            self.route_planning(self.ui.lineEdit_start.text(), self.ui.lineEdit_stop.text(), type)
        except:
            self.ui.route_text.setText("请选择其他出行方式")

    def routePlaning(self,res:list[str]):
        res = '\n'.join(res)
        print(res)
        self.ui.route_text.setPlainText(res)

    # 切换tabWidget动作
    def Change2Tab_folium(self):
        self.ui.tabWidget.setCurrentIndex(1)

    def Change2Tab_mapCanvas(self):
        self.ui.tabWidget.setCurrentIndex(0)

    # 获取属性文件(音视频）
    def addMusicPath(self):
        fp = self.getFilePath('m')
        self.feat.setPath("m",fp)
        self.musicPlayer_form.init_list(fp)

    def addVideoPath(self):
        fp = self.getFilePath('v')
        self.feat.setPath("v", fp)
        self.videoPlayer_form.init_list(vlist=fp)

    def addPicPath(self):
        fp = self.getFilePath('p')
        self.feat.setPath("p", fp)
        self.pictures=fp
        self.setPicture()

    def getFilePath(self,filetype):
        dic = {'p': "(*.png);(*.jpg)", 'm': "(*.mp3)", "v": "*.mp4"}
        # 获得的是电脑的绝对路径
        files, _ = QFileDialog.getOpenFileNames(self,
                                                  "多文件选择",
                                                  "./",
                                                  dic[filetype])
        # 放入json文件中
        return files

    # 文字编辑
    def getFeatureText2subMW(self):
        """
        初始在子窗口显示已编辑的文字
        :return:
        """
        txtHtml = self.ui.feat_showText.toHtml()
        self.textEditor_form.setHtmlTxt(txtHtml)

    def saveFeatureText(self):
        txtHtml = self.textEditor_form.ui.textEdit.toHtml()
        self.ui.feat_showText.setText(txtHtml)
        self.feat.setText(txtHtml)

    # 照片
    def setPicture(self):
        if self.pictures==[]:
            self.ui.label_Picture.setPixmap(QPixmap('./images/图片加载失败.png'))
            self.ui.label_Picture.setScaledContents(True)
            return
        # self.pictures = self.feat.getPath('p')
        self.picLoop = self.picLoop % len(self.pictures)
        # self.pictures = ['D:/0000Learning2022.9-1/GIS开发期末大作业/App/demo/picture/demo2.jpg', 'D:/0000Learning2022.9-1/GIS开发期末大作业/App/demo/picture/demo3.jpg', 'D:/0000Learning2022.9-1/GIS开发期末大作业/App/demo/picture/demo1.jpg']
        self.ui.label_Picture.setPixmap(QPixmap(self.pictures[self.picLoop]))
        self.ui.label_Picture.setScaledContents(True)

    def pre_pic(self):
        try:
            if self.pictures == []:
                print('请添加图片')
                return
            self.picLoop-=1
            self.setPicture()
        except:
            return

    def next_pic(self):
        try:
            if self.pictures == []:
                QMessageBox.warning(None, '提示', '请添加图片!', QMessageBox.Ok)
                return
            self.picLoop += 1
            self.setPicture()
        except:
            return

    def zoom_to_poi(self, name, lat, lon, zoom):
        map = self.Map.zoom_to_location(name, lat, lon, zoom)
        html = map.get_root().render()

        # 显示地图
        self.webview.setHtml(html)

    def show_map(self):

        # 生成地图
        self.map.init_map()
        self.map.add_polygons()
        self.map.add_markers()

        # 获取地图对象
        folium_map = self.map.m

        # 渲染为HTML
        html = folium_map.get_root().render()

        # 4. 根据中心点和缩放级别设置视角
        #center = self.map.center
        #zoom = self.map.zoom
        #folium_map.set_view(center, zoom)

        # 将HTML添加到QWebEngineView
        self.webview.setHtml(html)

        # 显示webview
        self.webview.show()



    #def InitMap(self):
    #    m = folium.Map(location=[39.907691, 116.39746], zoom_start=12,
    #                   tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    #                   attr='default')
    #    data = io.BytesIO()
    #    m.save(data, close_file=False)
    #    return data, m

    def smart_search(self, items_list):
        # 增加自动补全
        self.completer = QCompleter(items_list)
        # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        self.completer.setFilterMode(Qt.MatchContains)
        # 设置补全模式  有三种： QCompleter.PopupCompletion（默认)QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # 给lineedit设置补全器
        self.ui.endlineEdit.setCompleter(self.completer)

    def getstartxy(self):
        a = self.ui.startlineEdit.text()
        gd = GeographicCoding.GeographicCoding()
        code = gd.get_geographic_coding(a, '北京')
        p = gd.parse_geographic_coding(code)
        xy = p['geographic_position']
        c = []
        c = xy.split(',')
        lon = c[0]
        lat = c[1]
        self.ZoomMmap(a, lat, lon, 16)

    def getendxy(self):
        """
    #     已得到一个地名和坐标信息，首先判断它在不在标记的点里，若在标记的点里显示已标记的信息；
    #     若不在标记的点里，先初始化地名、坐标、时间，其他先不用搞
    #     :return:
    #     """
        self.place_now = self.ui.endlineEdit.text()
        print(self.place_now)
        try:
            gd = GeographicCoding.GeographicCoding()
            code = gd.get_geographic_coding(self.place_now, '北京')
            p = gd.parse_geographic_coding(code)
            xy = p['geographic_position']
            c = []
            c = xy.split(',')
            self.lon = c[0]
            self.lat = c[1]
            return self.lat,self.lon
        except:
            QMessageBox.warning(None, '提示', '地理编码错误！请检查网络', QMessageBox.Ok)
            return -1,-1

        # 如果用户标记过，则初始化地点信息，若未标记过则显示基础的经纬度、时间、地名三个信息。
        # if self.feat.isInFeatures(self.place_now):
        #     (self.lon, self.lat) = self.feat.getXY()
        #     self.showFeatures(self.place_now,self.lat,self.lon)
        #     self.ZoomMmap(self.place_now, self.lat, self.lon, 15)
        # else:
        #     gd = GeographicCoding.GeographicCoding()
        #     code = gd.get_geographic_coding(self.place_now, '北京')
        #     p = gd.parse_geographic_coding(code)
        #     xy = p['geographic_position']
        #     c = []
        #     c = xy.split(',')
        #     self.lon = c[0]
        #     self.lat = c[1]
        #     self.ZoomMmap(self.place_now, self.lat, self.lon, 15)
        #     time = datetime.now()
        #     today = (time.strftime('%Y-%m-%d'))
        #     print(today, self.lat, self.lon)
        #
        #     # 显示时间
        #     self.ui.timelineEdit.setText(today)
        #     # 显示经纬度
        #     self.ui.posilineEdit.setText(self.lon + ',' + self.lat)
        #     # 显示地名
        #     self.setPlaceNow_dock()

    def update_feature(self):
        """
        添加未标记点到用户数据里，添加其他信息
        :return
        """
        # self.place_now = self.ui.endlineEdit.text()
        if self.feat.isInFeatures(self.place_now):
            self.feat.save2json()
            self.ui.checkBox.setPixmap(QPixmap("./images/已标记.png"))
            self.ui.checkBox.setScaledContents(True)
        else:
            QMessageBox.warning(None, '提示', '该地点未标记过!', QMessageBox.Ok)
            return

    def addPoint2UserData(self):
        """
        添加未标记点到用户数据里，相当于初始化
        :return:
        """
        # self.place_now = self.ui.endlineEdit.text()
        if self.feat.isInFeatures(self.place_now):
            QMessageBox.warning(None, '提示', '该地点已经标记过了!', QMessageBox.Ok)
            return
        else:
            try:
                time = self.ui.timelineEdit.text().split('-')
                loc = self.ui.posilineEdit.text().split(',')
                self.place_now=self.ui.endlineEdit.text()
                y = int(time[0])
                m = int(time[1])
                d = int(time[2])
                state = self.feat.addPoint(self.place_now,float(loc[0]),float(loc[1]),[y,m,d])
                # self.addPoint2POI()  #TODO:如果要加在POI里的话
                self.ui.checkBox.setPixmap(QPixmap("./images/已标记.png"))
                self.ui.checkBox.setScaledContents(True)
            except:
                QMessageBox.warning(None, '提示', '添加发生错误！', QMessageBox.Ok)

    def showFeatures(self):
        self.ui.dockWidget_feature.show()
        self.place_now = self.ui.endlineEdit.text()
        if self.place_now=='':
            QMessageBox.warning(None, '提示', '请输入要查询的地点！', QMessageBox.Ok)
            return
        try:
            if self.feat.isInFeatures(self.place_now):
                self.ui.checkBox.setPixmap(QPixmap("./images/已标记.png"))
                self.ui.checkBox.setScaledContents(True)
                # 地名
                self.place_now = self.ui.endlineEdit.text()
                self.feat.setFeat_now(self.place_now)
                self.ui.feat_name_D1.setText(self.feat.getPlace_name())
                # 经纬度
                (self.lon,self.lat)=self.feat.getXY()  # 不再经过地理编码，地理编码时间较长且需要网络连接
                self.ui.posilineEdit.setText(str(self.lon) + ','+ str(self.lat))
                # 文字
                txt = self.feat.getText()
                # self.ui.feat_showText.setText(txt)
                self.ui.feat_showText.setHtml(txt)
                # 时间
                time = self.feat.getTime()
                time = f"{time[0]}-{time[1]}-{time[2]}"
                self.ui.timelineEdit.setText(time)
                # 图片
                self.pictures = self.feat.getPath('p')
                self.setPicture()
                # 音频
                mus = self.feat.getPath('m')
                self.musicPlayer_form.init_list(mus)
                # 视频
                vid = self.feat.getPath('v')
                self.videoPlayer_form.init_list(vid)
            else:
                self.lat, self.lon= self.getendxy()
                if self.lat == -1:
                    return
                self.ui.checkBox.setPixmap(QPixmap("./images/未标记.png"))
                self.ui.checkBox.setScaledContents(True)
                self.ui.feat_name_D1.setText(self.place_now)
                # 地名
                self.place_now = self.ui.endlineEdit.text()
                self.ui.feat_name_D1.setText(self.place_now)
                # 经纬度
                self.ui.posilineEdit.setText(self.lon + ',' + self.lat)
                # 时间
                time = datetime.now()
                today = (time.strftime('%Y-%m-%d'))
                self.ui.timelineEdit.setText(today)
                # 文字
                self.ui.feat_showText.setText('暂无游记~')
                # 图片
                self.ui.label_Picture.setPixmap(QPixmap('./images/图片加载失败.png'))
                self.ui.label_Picture.setScaledContents(True)

            # 地图显示缩放到搜索的地点
            self.ZoomMmap(self.place_now, self.lat, self.lon, 15)
        except:
            QMessageBox.warning(None, '提示', '属性显示异常！', QMessageBox.Ok)

    def addPoint2POI(self):
        """
        把标注的点信息放入POI表格中，可能这个点已经在POI里边了，如果在的话直接ruturn，不在的话添加点
        可以先不写，不太重要
        :return:
        """
        pass

    def route_planning(self, a, b, type):
        gdb = GeographicCoding.GeographicCoding()
        codeb = gdb.get_geographic_coding(a, '北京')
        pb = gdb.parse_geographic_coding(codeb)
        from_location = pb['geographic_position']
        cb = []
        cb = from_location.split(',')
        cblat = float(cb[1])
        cblon = float(cb[0])

        gda = GeographicCoding.GeographicCoding()
        codea = gda.get_geographic_coding(b, '北京')
        pa = gda.parse_geographic_coding(codea)
        to_location = pa['geographic_position']
        ca = []
        ca = to_location.split(',')
        calat = float(ca[1])
        calon = float(ca[0])
        lat = (calat + cblat) / 2
        lon = (calon + cblon) / 2
        mapcenter = [lat, lon]
        geourl = 'https://a.amap.com/jsapi_demos/static/geojson/beijing.json'
        geostyle = lambda x: {'fillColor': '#0000ff', 'fillOpacity': 0.2, 'line_opacity': 0.2}
        zoom = 12
        url="https://restapi.amap.com"
        if type=="1":
            url = url+ "/v3/direction/transit/integrated"
        elif type=="2":
            url = url + "/v3/direction/walking"
        elif type=="3":
            url = url + "/v3/direction/driving"
        elif type == "4":
            url = url + "/v4/direction/bicycling"
        parameters = {
            'key': 'b93bd3b29466cf3feece0ce075f5f0b4',
            'origin': str(from_location),
            'destination': str(to_location),
            'extensions':'all',
            'output':'json',
            'city':'020',
        }

        d=[]
        response = requests.get(url, parameters)
        txt = json.loads(response.text)
        #print(txt)
        if type=="1":
            bus_origin_float = txt['route']['origin'].split(',')[1].split(" ") + txt['route']['origin'].split(',')[0].split(" ")
            bus_origin = [float(x) for x in bus_origin_float]
            bus_destination_float = txt['route']['origin'].split(',')[1].split(" ") + txt['route']['origin'].split(',')[0].split(" ")
            bus_destination = [float(x) for x in bus_destination_float]
            txt = txt['route']['transits']
            for i in range(len(txt)):
                for j in range(len(txt[i]['segments'][0]['bus']['buslines'][0]['polyline'].split(';'))):
                    bus_location_1 = txt[i]['segments'][0]['bus']['buslines'][0]['polyline'].split(';')[j]
                    bus_location_float = bus_location_1.split(',')[1].split(" ") + bus_location_1.split(',')[0].split(
                        " ")
                    bus_location_int = [float(x) for x in bus_location_float]
                    d.append(bus_location_int)
            d.insert(0, bus_origin)
            d.append(bus_destination)

        elif type=="2":
            walk_origin_float = txt['route']['origin'].split(',')[1].split(" ") + txt['route']['origin'].split(',')[0].split(" ")
            walk_origin = [float(x) for x in walk_origin_float]
            walk_destination_float = txt['route']['origin'].split(',')[1].split(" ") + txt['route']['origin'].split(',')[0].split(" ")
            walk_destination = [float(x) for x in walk_destination_float]
            txt = txt['route']['paths'][0]['steps']
            for i in range(len(txt)):
                for j in range(len(txt[i]['polyline'].split(';'))):
                    walk_location_1 = txt[i]['polyline'].split(';')[j]
                    walk_location_float = walk_location_1.split(',')[1].split(" ") + walk_location_1.split(',')[0].split(
                        " ")
                    walk_location_int = [float(x) for x in walk_location_float]
                    d.append(walk_location_int)
            d.insert(0, walk_origin)
            d.append(walk_destination)

        elif type=="3":
            drive_origin_float = txt['route']['origin'].split(',')[1].split(" ") + txt['route']['origin'].split(',')[0].split(" ")
            drive_origin = [float(x) for x in drive_origin_float]
            drive_destination_float = txt['route']['destination'].split(',')[1].split(" ") + txt['route']['destination'].split(',')[0].split(" ")
            drive_destination = [float(x) for x in drive_destination_float]
            txt = txt['route']['paths'][0]['steps']
            for i in range(len(txt)):
                for j in range(len(txt[i]['polyline'].split(';'))):
                    drive_location_1 = txt[i]['polyline'].split(';')[j]
                    drive_location_float = drive_location_1.split(',')[1].split(" ") + drive_location_1.split(',')[0].split(" ")
                    drive_location_int = [float(x) for x in drive_location_float]
                    d.append(drive_location_int)
            d.insert(0, drive_origin)
            d.append(drive_destination)

        elif type == "4":
            ride_origin_float = txt['data']['origin'].split(',')[1].split(" ") + txt['data']['origin'].split(',')[0].split(" ")
            ride_origin = [float(x) for x in ride_origin_float]
            ride_destination_float = txt['data']['origin'].split(',')[1].split(" ") + txt['data']['origin'].split(',')[0].split(" ")
            ride_destination = [float(x) for x in ride_destination_float]
            txt = txt['data']['paths'][0]['steps']
            for i in range(len(txt)):
                for j in range(len(txt[i]['polyline'].split(';'))):
                    ride_location_1 = txt[i]['polyline'].split(';')[j]
                    ride_location_float = ride_location_1.split(',')[1].split(" ") + ride_location_1.split(',')[0].split(
                        " ")
                    ride_location_int = [float(x) for x in ride_location_float]
                    d.append(ride_location_int)
            d.insert(0, ride_origin)
            d.append(ride_destination)
        mmap2 = MyMap(mapcenter, self.pointdata, geourl, geostyle, zoom)  # 底图对象
        m2 = mmap2.m
        ls = folium.PolyLine(locations=d, color='red')
        ls.add_to(m2)

        m2.save('test.html')
        self.webview.load(QUrl(mmap2.get_mapurl()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_form = appMainWindow()  # 主窗体

    # 主窗体
    main_form.show()
    sys.exit(app.exec_())
