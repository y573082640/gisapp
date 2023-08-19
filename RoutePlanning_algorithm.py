import requests
import json

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
def route_planning(from_place,to_place,type):
    print(f"从{from_place}到{to_place}")
    # from_place = input("请输入起始地址")
    from_location = get_location_x_y(from_place)
    # to_place = input("请输入目的地")
    to_location = get_location_x_y(to_place)
    # type = input("出行方式（1.公交、2.步行、3.驾车、4.骑行）,请输入数字")
    url="https://restapi.amap.com"
    if type==1:
        url = url+ "/v3/direction/transit/integrated"
    elif type==2:
        url = url + "/v3/direction/walking"
    elif type==3:
        url = url + "/v3/direction/driving"
    elif type ==4:
        url = url + "/v4/direction/bicycling"
    parameters = {
        'key': 'b93bd3b29466cf3feece0ce075f5f0b4',
        'origin': str(from_location),
        'destination': str(to_location),
        'extensions':'all',
        'output':'json',
        'city':'020',
    }

    response = requests.get(url, parameters)
    txt = json.loads(response.text)
    # print(txt)
    route_text = []

    if txt['status'] == '0':
        print('未查询到路线，请输入正确地名...')
        return
    if type==1:
        txt = txt['route']['transits']
        for i in txt:
            i = i['segments'][0]['bus']['buslines'][0]['name']
            route_text.append(i)
            # print(i)
        return route_text
    elif type==2:
        txt = txt['route']['paths'][0]['steps']
        for i in txt:
            i = i['instruction']
            route_text.append(i)
            # print(i)
        return route_text
    elif type==3:
        txt = txt['route']['paths'][0]['steps']
        for i in txt:
            i = i['instruction']
            route_text.append(i)
        return route_text
    elif type == 4:
        txt = txt['data']['paths'][0]['steps']
        for i in txt:
            i = i['instruction']
            route_text.append(i)
        return route_text
    else:
        return "未搜索到路线,请输入正确地名"


if __name__ == '__main__':
    route_planning("北京师范大学","北京西站",1)