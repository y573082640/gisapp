# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import time
import requests
from GCode import OfficialException, CustomExpection
from GCode import WriteLog

# Model 层

class GeographicCodingModel:

    def __init__(self, address, city):
        self.address = address
        self.city = city

    def get_geographic_coding(self, address: str,
                              city: str,
                              **kwargs
                              ) -> dict:
        """
        函数：获取地理编码数据。\n
        Args:
            address:结构化地址信息，必填。规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。如果需要解析多个地址的话，请用"|"进行间隔，并且将 batch参数设置
                    为 true，最多支持 10 个地址进进行"|"分割形式的请求。
            city:指定查询的城市，可选。可选输入内容包括：指定城市的中文（如北京）、指定城市的中文全拼（beijing）、citycode（010）、adcode（110000），不支持县级市。当指定城市查询内容为空时，会进行全国范围内的地址转换检索。
            kwargs:
                output:返回数据格式类型，可选，默认JSON格式。可选输入内容包括：JSON，XML。设置 JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。
                batch:批量查询控制，可选，默认False。batch 参数设置为 true 时进行批量查询操作，最多支持 10 个地址进行批量查询。batch 参数设置为 false 时进行单点查询，此时即使传入多个地址也只返
                    回第一个地址的解析查询结果。
        Returns:返回获得的json格式数据或错误信息
        """

        self.address = address
        self.city = city

        if 'batch' in kwargs:
            self.batch = kwargs['batch']
        if 'output' in kwargs:
            self.output = kwargs['output']

        # 写入日志
        writeLog = WriteLog.WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'address': self.address,
                      'city': self.city
                      }

        if self.batch is not None:
            parameters.update(batch=self.batch)
        if self.output is not None:
            parameters.update(output=self.output)

        # 获取数据
        try:
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            request_information = requests.get("https://restapi.amap.com/v3/geocode/geo?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # 返回格式化后的JSON数据
            json_decode = json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Geographic coding data successful get.'.format(
                                      function_name)
                                  )
            return json_decode

        except requests.exceptions.ConnectionError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_connection = 'ConnectionError -- please wait 3 seconds'
            error_connection_dict = {'status': '2',
                                     'info': 'requests.exceptions.ConnectionError',
                                     'detail_information': requests.exceptions.ConnectionError,
                                     'error_prompt': error_connection
                                     }
            return error_connection_dict

        except requests.exceptions.ChunkedEncodingError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
            error_chuck_encoding_dict = {'status': '2',
                                         'info': 'HTTPError',
                                         'detail_information': requests.exceptions.ChunkedEncodingError,
                                         'error_prompt': error_chuck_encoding
                                         }
            return error_chuck_encoding_dict

        except Exception as e:
            time.sleep(1)
            error_information = 'Unfortunately -- An unknown Error Happened, Please wait 3 seconds'
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_information_dict = {'status': '2',
                                      'info': 'HTTPError',
                                      'detail_information': requests.exceptions.ChunkedEncodingError,
                                      'error_prompt': error_information
                                      }

            return error_information_dict
        #pass

    def get_inverse_geographic_coding(self, location: str,
                                      **kwargs
                                      ) -> dict:

        """
        函数：获取逆地理编码数据。\n
        Args:
            location:经纬度坐标，必填。传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。如果需要解析多个经纬度的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最
                    多支持传入 20 对坐标点。每对点坐标之间用"|"分割。
            kwargs:
                radius:搜索半径，可选，默认1000。radius取值范围在0~3000。单位：米。
                roadLevel:道路等级，可选。以下内容需要 extensions 参数为 all时才生效。可选值：0，1当roadlevel=0时，显示所有道路。当roadlevel=1时，过滤非主干道路，仅输出主干道路数据。
                extensions:返回结果控制，可选，默认base。extensions 参数默认取值是 base，也就是返回基本地址信息；extensions 参数取值为 all 时会返回基本地址信息、附近 POI内容、道路信息以及道路交叉
                        口信息。
                poitype:返回附近POI类型，可选。以下内容需要 extensions 参数为 all 时才生效。逆地理编码在进行坐标解析之后不仅可以返回地址描述，也可以返回经纬度附近符合限定要求的POI内容（在
                        extensions 字段值为 all 时才会返回POI内容）。设置 POI 类型参数相当于为上述操作限定要求。参数仅支持传入POI TYPECODE，可以传入多个POITYPECODE，相互之间用“|”分隔。该参
                        数在 batch 取值为 true 时不生效。
                output:返回数据格式类型，可选，默认JSON格式。可选输入内容包括：JSON，XML。设置JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。
                batch:批量查询控制，可选，默认False。batch 参数设置为 true 时进行批量查询操作，最多支持 20 个经纬度点进行批量地址查询操作。batch 参数设置为 false 时进行单点查询，此时即使传入多个经纬度也只返回第一个
                        经纬度的地址解析查询结果。
                homeorcorp:是否优化POI返回顺序，可选，默认0。以下内容需要 extensions 参数为 all时才生效。homeorcorp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：0：不对召回
                        的排序策略进行干扰。1：综合大数据分析将居家相关的 POI 内容优先返回，即优化返回结果中 pois字段的poi顺序。2：综合大数据分析将公司相关的 POI 内容优先返回，即优化返回结果中 pois
                        字段的poi顺序。
        Returns:返回获得的json格式数据或错误信息
        """

        self.location = location

        if 'batch' in kwargs:
            self.batch = kwargs['batch']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'homeorcorp' in kwargs:
            self.homeorcrop = kwargs['homeorcorp']
        if 'poitype' in kwargs:
            self.poitype = kwargs['poitype']
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
        if 'roadlevel' in kwargs:
            self.roadLevel = kwargs['roadlevel']

        # 写入日志
        writeLog = WriteLog.WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': GeographicCodingModel.APIkey,
                      'location': self.location,
                      }

        if self.batch is not None:
            parameters.update(batch=self.batch)
        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.homeorcrop is not None:
            parameters.update(homeorcorp=self.homeorcrop)
        if self.poitype is not None:
            parameters.update(poitype=self.poitype)
        if self.radius is not None:
            parameters.update(radius=self.radius)
        if self.roadLevel is not None:
            parameters.update(roadlevel=self.roadLevel)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/geocode/regeo?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            inverse_json_decode = json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Inverse geographic coding data successful get.'.format(
                                      function_name)
                                  )
            return inverse_json_decode

        except requests.exceptions.ConnectionError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )

            # 异常信息
            error_connection = 'ConnectionError -- please wait 3 seconds'
            error_connection_dict = {'status': '2',
                                     'info': 'requests.exceptions.ConnectionError',
                                     'detail_information': requests.exceptions.ConnectionError,
                                     'error_prompt': error_connection
                                     }

            return error_connection_dict

        except requests.exceptions.ChunkedEncodingError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )

            # 异常信息
            error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
            error_chuck_encoding_dict = {'status': '2',
                                         'info': 'HTTPError',
                                         'detail_information': requests.exceptions.ChunkedEncodingError,
                                         'error_prompt': error_chuck_encoding
                                         }

            return error_chuck_encoding_dict

        except Exception as e:
            time.sleep(1)
            # only for debugging
            error_information = 'Unfortunately -- An unknown Error Happened, Please wait 3 seconds'
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )

            # 异常信息
            error_information_dict = {'status': '2',
                                      'info': 'HTTPError',
                                      'detail_information': requests.exceptions.ChunkedEncodingError,
                                      'error_prompt': error_information
                                      }

            return error_information_dict
        #pass

# View 层

class GeographicCodingView:

    def show_geographic_coding_result(self, result):
        print(result)

    def show_inverse_geographic_coding_result(self, result):
        print(result)

# Controller 层

class GeographicCodingController:

    def __init__(self):
        self.model = GeographicCodingModel()
        self.view = GeographicCodingView()

    def get_geographic_coding(self, address, city):
        result = self.model.get_geographic_coding(address, city)
        self.view.show_geographic_coding_result(result)

    def get_inverse_geographic_coding(self, location):
        result = self.model.get_inverse_geographic_coding(location)
        self.view.show_inverse_geographic_coding_result(result)

# 主程序

#controller = GeographicCodingController()
#controller.get_geographic_coding("北京市海淀区上地十街10号", "北京")
#controller.get_inverse_geographic_coding("39.983424,116.322987")




