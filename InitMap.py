import io, sys, folium
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl
import os

class MyMap():
    def __init__(self, center, pointdata, geourl, geostyle, zoom):
        self.center = center  # 这里是生成地图中心坐标
        self.pointdata = pointdata  # 位置信息，这个是那个xls文件内的数据，你可以通过更改对应的xls内的数据处理点
        self.geourl = geourl  # 这是行政区域几何边界的url网址
        self.geostyle = geostyle  # 这个不清楚，但不重要
        self.zoom = zoom  # 初始大小
        self.data, self.m = self.InitMapshow()  # 显示行政边界，用folium画多边形，输入json网址
        self.point_show()  # 显示点
        self.__url = self.get_mapurl()

# 在地图上显示行政边界
    def InitMapshow(self):
        m = folium.Map(location=self.center, zoom_start=self.zoom,
        tiles=None,
        control_scale=True)
        data = io.BytesIO()
        m.save(data, close_file=False)
        folium.TileLayer(tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}',
                        attr='彩色版').add_to(m)
        # folium.TileLayer(tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'
        #                  , attr='default', name='高德地图').add_to(m)  # 地图瓦片添加命名
        # https://cloud.tencent.com/developer/article/1919827 不同的底图瓦片效果选择
        # 添加geojson到地图
        folium.GeoJson(
            self.geourl,
            name='行政区边界',
            style_function=self.geostyle
        ).add_to(m)
        return data, m

# 显示点
    def point_show(self):
        data = self.pointdata
        #聚类显示
        distriction = data['DISTRICT'].drop_duplicates()  # 聚类是一个区一类
        #创建组
        for i in distriction:
            exec(str(i) + ' = ' + 'FeatureGroup(name="' + str(i) + '",show=True).add_to(self.m)')
        # 创建聚合
        for j in distriction:
            exec(str(j) + 'mc = ' + 'MarkerCluster().add_to(' + str(j) + ')')
        # marker_cluster = MarkerCluster().add_to(self.m)
        htmlname = "test.html"
        for i in range(len(data['X'])):
            exec('''folium.Marker(
                location=[data['Y'][i], data['X'][i]],
                popup=folium.Popup(folium.Html(
                '<b>名称:{}</b></br> <b>地址:{}</b></br> <b>经度:{}</b></br> <b>纬度:{}</b></br>'
                .format(data['NAME'][i], data['ADRESS'][i], data['X'][i], data['Y'][i]),
                script=True), max_width=2650),icon=folium.Icon(color='gray')
            ).add_to('''+str(data.loc[i, 'DISTRICT'])+'mc)')  # 这里是画点的区域，这个exec函数是没看懂，但大概可以把里面的内容看成folium画点
        LayerControl(collapsed=True).add_to(self.m)

# 这个不重要
    def get_mapurl(self):
        htmlname = "test.html"
        self.m.save(htmlname)
        path = "file:\\" + os.getcwd() + "\\test.html"
        path = path.replace('\\', '/')
        return path



