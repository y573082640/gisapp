import io, sys, folium
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl
import os


class MyMap():

    def __init__(self, center, pointdata, geourl, geostyle, zoom):
        self.center = center
        self.pointdata = pointdata
        self.geourl = geourl
        self.geostyle = geostyle
        self.zoom = zoom
        self.m = self.init_map()
        self.add_polygons()
        self.add_markers()
        self.get_map_url()
        self.data = None

    def init_map(self):
        m = folium.Map(location=self.center, zoom_start=self.zoom)
        # 初始化地图
        return self.get_base_map(m)

    def get_base_map(self, m):
        data = io.BytesIO()
        m.save(data, close_file=False)
        folium.TileLayer(
            tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}',
            attr='彩色版').add_to(m)
        return data, m

    def add_polygons(self):
        # 添加行政区边界多边形
        folium.GeoJson(
            self.geourl,
            name='行政区边界',
            style_function=self.geostyle
        ).add_to(self.m)

    def add_markers(self):
        # 添加 Marker 和 MarkerCluster
        data = self.pointdata
        distriction = data['DISTRICT'].drop_duplicates()

        for district in distriction:
            fg = FeatureGroup(name=district, show=True).add_to(self.m)
            mc = MarkerCluster().add_to(fg)

            for i in range(len(data['X'])):
                self.add_marker(district, mc, i)

        LayerControl(collapsed=True).add_to(self.m)

    def add_marker(self, district, mc, i):
        # 添加单个 Marker
        folium.Marker(
            location=[self.data['Y'][i], self.data['X'][i]],
            popup=folium.Popup(content=self.get_popup_content(i)),
            icon=folium.Icon(color='gray')
        ).add_to(mc)

    def get_popup_content(self, i):
        # 获取 popup 内容
        return folium.Html('''
            <b>名称:{}</b></br> 
            <b>地址:{}</b></br>
            <b>经度:{}</b></br>
            <b>纬度:{}</b></br>
        '''.format(self.data['NAME'][i], self.data['ADRESS'][i], self.data['X'][i], self.data['Y'][i]),
                           script=True)

    def get_map_url(self):
        # 获取地图 URL
        htmlname = "test.html"
        self.m.save(htmlname)
        path = "file:\\" + os.getcwd() + "\\test.html"
        return path.replace('\\', '/')