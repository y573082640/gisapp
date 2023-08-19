# -*- coding : utf-8 -*-
# @Author : Dynamt
# @Time: 2023-01-16 19:25
# 功能实现 ：将地点信息展示的所有信息数据整理成类
import glob,os,json

class FeatureInfo():
    def __init__(self,user_ID:str):
        """
        :param feat_name:每个点要素的地名，通过地名索引下面的属性字典
        将地点信息展示的所有信息数据整理成类,整理完成便于主程序调用，每变换新的点就刷新修改,一个点有一个data，需要储存和写入
        :return data: 字典类型数据，包括
        ”state“:是否游历过或创建标记过
        ”place":地名，通过搜索框
        ”locationXY“:xy坐标元组，(x,y)
        “time”:游历的时间，用户标记点的时候自己输入储存
        “text":记录游历的文字（带格式与否需要考虑）
        ”pic_paths":照片的路径，list[str],需要打开及展示在dockwidget中
        “video_paths":视频路径列表，需要获取和添加
        ”music_paths“:音频路径列表，需要获取和修改
        """
        self.feat_name="北京师范大学"
        self.user_ID = user_ID
        self.__init()
        # self.userData_path = './userData/user.001.json'
        """
        "\u5317\u4eac\u5e08\u8303\u5927\u5b66": {"state": false, "place": "\u5317\u4eac\u5e08\u8303\u5927\u5b66", "locationXY": {"X": 0, "Y": 0}, "time": [2022, 12, 28], "date": 20221228, "text": "2022,3,4", "pic_paths": [], "music_paths": [], "video_paths": []}}
        """


    def setFeat_now(self,name):
        if self.isInFeatures(name):
            self.feat_name =name
            self.__init()
        else:
            print("该地点未标记")
            return

    def isInFeatures(self,name):
        if name in self.points.keys():
            return True
        else:
            return False

    def __readJson(self):
        try:
            with open(self.userData_path,'r',encoding='utf-8') as fp:
                self.user_json = json.load(fp)
                self.points = self.user_json["points"]
                self.feat_now = self.user_json["points"][self.feat_name]
        except:
            print("读取用户文件错误,请确保用户数据文件存在并格式正确")
            return

    def __init(self):
        """
        在登录时初始化用户信息，获得一个json文件用于储存用户信息。
        现在程序运行要提取出来。
        :return:
        """
        # self.userData_path = glob.glob(f"D:\\0000Learning2022.9-1\\GIS开发期末大作业\\App\\userData\\{self.user_ID:03d}*.json")[0]
        self.userData_path=f"./userData/user.{self.user_ID}.json"    # TODO:固定命名形式，要不然得改这一部分
        if os.path.exists(self.userData_path):
            self.__readJson()

    # 地名
    def setPlace_name(self,place):
        """
        从搜索框里得到名字，放入字典中
        :return:
        """
        self.feat_now['place']=place
        self.points.pop(self.feat_name)
        self.feat_name = place
        self.points[self.feat_name]=self.feat_now

    def getPlace_name(self):
        """
        从字典中得到
        :return:
        """
        return self.feat_now['place']

    def setXY(self,x,y):
        self.feat_now['locationXY']['X']=x
        self.feat_now['locationXY']['Y']=y
        self.points[self.feat_name] = self.feat_now

    def getXY(self):

        return self.feat_now['locationXY']['X'], self.feat_now['locationXY']['Y']

    def setTime(self,y,m,d):
        y = int(y)
        m = int(m)
        d = int(d)
        self.feat_now['time'] = [y, m, d]
        self.feat_now['date'] = y * 10000 + m * 100 + d
        self.points[self.feat_name] = self.feat_now

    def getTime(self):
        return self.feat_now['time']

    def setText(self,txt):
        """"
        每次编辑文字之后储存文字
        """
        self.feat_now['text'] = txt
        self.points[self.feat_name] = self.feat_now

    def getText(self):
        """
        每次更新地点信息时，更新显示
        :return:
        """
        return self.feat_now['text']

    def setPath(self,pathType,fp:list):
        """
        :param pathType: v/p/m  'p':"pic_paths",'v':"video_paths","m":"music_paths"
        :return: list
        """
        try:
            fp_set = set(fp)
            ori_set = set(self.feat_now[pathType])
            self.feat_now[pathType] = list(fp_set | ori_set)
            self.points[self.feat_name] = self.feat_now
        except:
            print("设置路径错误")
            return

    def getPath(self,pathType):
        """
        :param pathType: v/p/m  'p':"pic_paths",'v':"video_paths","m":"music_paths"
        :return: list
        """

        return self.feat_now[pathType]

    def addPoint(self,name:str,locX,locY,time:list,txt="暂无",pic:list=[],mus=[],vid=[]):   # TODO：增加新点
        """
        添加点到用户数据中，必须输入地名，若地名已被标记到json中则范围添加失败已存在标记点
        :param name:
        :param locX:
        :param locY:
        :param time:
        :param txt:
        :param pic:
        :param mus:
        :param vid:
        :return: 添加是否成功
        """
        if self.isInFeatures(name):
            return False
        new_point_info = {"state": 1,"place": name,"locationXY": {"X": locX,"Y": locY},"time": time,"date": 20221228,"text": txt,"p": pic,"m": mus,"v": vid}
        self.points[name] = new_point_info
        self.save2json()
        return True

    def save2json(self):
        """"
        点数据修改后保存
        """
        with open(self.userData_path,'w') as f:
            self.user_json["points"] = self.points
            json.dump(self.user_json, f)

    def delPoint(self,name):
        if self.isInFeatures(name):
            self.points.pop(name)
            self.save2json()
            self.feat_name = "北京师范大学"
            self.__init()
        else:
            print("地点未标记过")


if __name__ == '__main__':
    feat = FeatureInfo('GIS')
    feat.setPlace_name("北京师范大学")
    feat.isInFeatures("北京师范大学")
    feat.save2json()
    print(feat.getPath('v'))

