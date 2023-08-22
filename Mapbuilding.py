import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Map:

    def __init__(self, center, zoom):
        self.center = center
        self.zoom = zoom
        self.webview = QWebEngineView()

    def create_map(self):
        return folium.Map(location=self.center, zoom_start=self.zoom)

    def add_marker(self, map, name, lat, lon):
        marker = folium.Marker(location=[lat, lon],
                               popup=folium.Popup(name))
        marker.add_to(map)

    def zoom_to_location(self, name, lat, lon):
        map = self.create_map()
        self.add_marker(map, name, lat, lon)
        return map

    def show_map(self, map):
        html = map.get_root().render()
        self.webview.setHtml(html)
        self.webview.show()