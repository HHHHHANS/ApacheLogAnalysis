"""基础远程获取日志类"""
import requests
from common.common import Logger


class BaseRemoter:
    """远程获取日志基础类"""
    def __init__(self):
        pass


class ApacheLogRemoter(BaseRemoter):
    """从apache服务器获取日志数据"""

    def __init__(self,
                 host='localhost',
                 port=1111,
                 method='GET',
                 params=None,
                 **kwargs):
        super(BaseRemoter, self).__init__()
        self._host = host
        self._port = port
        self._params = params
        self._kwargs = kwargs
        self._data_checker = RemoteDataChecker()
        if method in ['get', 'GET', 'Get']:
            self.get()

    def safety_examination(self, data):
        """对远程获取的数据进行安全性校验
        raise 相应的安全错误
        """
        try:
            self._data_checker.check(data)
        except Exception as e:
            raise e

    def get(self):
        """调用 GET 方法获取远程数据"""
        result = requests.get(f'{self._host}:{self._port}', params=self._params)
        try:
            # 对获取的数据进行校验
            self.safety_examination(data=result)
            return result
        except Exception as e:
            raise e


class RemoteDataChecker:
    """对远程数据进行校验：安全性/完整性等"""

    def __int__(self):
        # TODO 模拟使用数据安全引擎
        self._data_engine = None

    def check(self, data):
        """对数据的安全检查和相关校验

        raise相应的错误类型
        """
        self._data_engine(data)



