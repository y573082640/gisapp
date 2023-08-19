import requests
import json
import folium
import os


#获取经纬度
def get_location_x_y(place):
    #place = input("请输入您要查询的地址")
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'key':'b93bd3b29466cf3feece0ce075f5f0b4',
        'address':'%s' % place
    }
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text       #获得数据是json格式
    data = json.loads(text)         #把数据变成字典格式
    location = data["geocodes"][0]['location']
    return location

#路线规划
def route_planning():
    from_place = input("请输入起始地址")
    from_location = get_location_x_y(from_place)
    to_place = input("请输入目的地")
    to_location = get_location_x_y(to_place)
    type = input("出行方式（1.公交、2.步行、3.驾车、4.骑行）,请输入数字")
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

    bus_location = []
    walk_location = []
    drive_location = []
    ride_location = []
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
                bus_location.append(bus_location_int)
        bus_location.insert(0, bus_origin)
        bus_location.append(bus_destination)
        return bus_location

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
                walk_location.append(walk_location_int)
        walk_location.insert(0, walk_origin)
        walk_location.append(walk_destination)
        return walk_location

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
                drive_location.append(drive_location_int)
        drive_location.insert(0, drive_origin)
        drive_location.append(drive_destination)
        return drive_location

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
                ride_location.append(ride_location_int)
        ride_location.insert(0, ride_origin)
        ride_location.append(ride_destination)
        return ride_location
