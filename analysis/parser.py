""" 文件内容解析模块"""
from config import SystemConfig
from common import Logger
from typing import List
import abc

# 需要过滤的资源类型
EXCLUDED_RES_TYPE = SystemConfig.TMP_excluded_res_type


class BaseParser:
    """日志内容解析基础类, 定义所有日志解析类需要继承"""

    def __init__(self):
        self._parse_result = list()

    @abc.abstractmethod
    def parse(self, file_lines: List[str]):
        """特定的解析过程

        :param file_lines: 文件读取行内容
        :return
        """
        pass

    @abc.abstractmethod
    def result(self):
        # """输出解析结果"""
        # return self._parse_result
        pass


class ApacheLogParser(BaseParser):
    """apache .log类日志解析程序基类， 所有apache日志解析类需要继承"""

    def __init__(self, version):
        self._producer = 'apache'
        self._log_file_suffix = '.log'
        self._version = version
        self._parse_method = None
        super(ApacheLogParser, self).__init__()

    def parse(self, file_lines: List[str]):
        pass

    def result(self):
        pass


class ApacheLog_V_1_1(ApacheLogParser):
    """
    apache v1.1版本 日志解析类
    Example:
    200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-fontsettings/website.css HTTP/1.1" 200 8596
    """

    def __init__(self):
        self.version = 1.1
        self._base_filed = ["request_ip",
                            "request_id",
                            "request_name",
                            "request_time",
                            "request_method",
                            "request_url",
                            "request_resource_type",
                            "request_params"
                            "request_protocol",
                            "request_protocol_version",
                            "response_status_code",
                            "response_bytes"]
        self._excluded_resource = EXCLUDED_RES_TYPE
        super(ApacheLog_V_1_1, self).__init__(self.version)

    def add_parser(self, key, method):
        """"""
        pass

    def parse(self, file_lines: List[str]):
        """接收字符串列表，遍历列表进行解析"""
        results = []
        for file_line in file_lines:
            try:
                row_info = self.parse_row(file_line)
                if row_info is None:
                    continue
                # print(row_info)
            except Exception as e:
                Logger.error(e)
                continue
            results.append(row_info)
        self._parse_result = results

    def parse_row(self, file_line: str):
        """解析一行日志字符串

        """

        # 该行日志所含元素
        row_info = {k: None for k in self._base_filed}

        if not isinstance(file_line, str):
            raise TypeError(f'should receive str of line, {type(file_line)} instead')
        for ignore_type in self._excluded_resource:
            if ignore_type in file_line:
                return None
        file_line = file_line.strip()
        self._parse_request_ip(file_line, row_info)

        return row_info

    def _parse_request_ip(self, part_file_line, row_info):
        """1.提取ip地址"""

        def __request_ip_is_valid(**kwargs):
            """内部验证"""
            return True

        part_file_line = part_file_line.lstrip()

        for cha_index in range(len(part_file_line)):
            # 第一个空格前为IP地址
            if part_file_line[cha_index] == ' ':
                request_ip = part_file_line[:cha_index]
                row_info['request_ip'] = request_ip if __request_ip_is_valid(request_ip=request_ip) else None
                self._parse_request_id(part_file_line[cha_index + 1:], row_info)
                return

        raise ValueError(f'parse request ip error')

    def _parse_request_id(self, part_file_line, row_info):
        """2.提取request id"""

        def __request_id_is_valid(**kwargs):
            return True

        part_file_line = part_file_line.lstrip()

        for cha_index in range(len(part_file_line)):
            if part_file_line[cha_index] == ' ':
                request_id = part_file_line[:cha_index]
                row_info['request_id'] = request_id if __request_id_is_valid(request_id=request_id) else None
                self._parse_request_name(part_file_line[cha_index + 1:], row_info)
                return

        raise ValueError(f'parse request id error')

    def _parse_request_name(self, part_file_line, row_info):
        """3.提取request name"""

        def __request_name_is_valid(**kwargs):
            """内部验证"""
            return True

        part_file_line = part_file_line.lstrip()
        for cha_index in range(len(part_file_line)):
            if part_file_line[cha_index] == ' ':
                request_name = part_file_line[:cha_index]
                row_info['request_name'] = request_name if __request_name_is_valid(request_name=request_name) else None
                self._parse_request_time(part_file_line[cha_index + 1:], row_info)
                return
        raise ValueError(f'parse request name error')

    def _parse_request_time(self, part_file_line, row_info):
        """4.提取request time"""

        def __request_time_is_valid(**kwargs):
            """内部验证"""
            return True

        def __parse_time(time_str: str):
            """具体提取日期"""
            time_info = time_str if __request_time_is_valid(request_time_str=request_time_str) else None
            return {'origin_time': time_info}

        part_file_line = part_file_line.lstrip()
        for cha_index in range(len(part_file_line)):
            if part_file_line[cha_index] == ']' and part_file_line[0] == '[':
                request_time_str = part_file_line[1:cha_index]
                request_time_dict = __parse_time(request_time_str)
                row_info['request_time'] = request_time_dict
                self._parse_request_method_url_ptl_version(part_file_line[cha_index + 1:], row_info)
                return

        raise ValueError(f'parse request time error')

    def _parse_request_method_url_ptl_version(self, part_file_line: str, row_info: dict):
        """5. 提取请求方法、url、资源类型、请求参数、协议及版本号"""

        def __request_method_is_valid(**kwargs):
            return True

        def __request_url_is_valid(**kwargs):
            return True

        def __request_protocol_is_valid(**kwargs):
            return True

        def __request_protocol_version_is_valid(**kwargs):
            return True

        def _parse_url_resource_type_and_params(url: str):
            """解析完整url，获得资源类型和请求参数"""
            request_res_type = None
            request_params = None

            sub_ele = url.split('?')
            if len(sub_ele) > 2:
                raise ValueError(f'more than two \'?\' in url: {url}')
            elif len(sub_ele) == 1:
                request_params = None
            if len(sub_ele) == 2:
                request_params = sub_ele[1]

            if '.' not in sub_ele[0]:
                if sub_ele[0] == '*':
                    request_res_type = None
                else:
                    raise ValueError(f'\'.\' not in url: {url}.')
            else:
                for i in range(len(sub_ele[0]) - 1):
                    if sub_ele[0][i] == '.':
                        request_res_type = sub_ele[0][i + 1:]

            return {'request_resource_type': request_res_type,
                    'request_params': request_params}

        part_file_line = part_file_line.lstrip()
        for cha_index in range(len(part_file_line)):
            part_file_line = part_file_line.lstrip()
            if part_file_line[cha_index] == '\"' and part_file_line[0] == '\"' and cha_index != 0:
                request_method_and_url_str = part_file_line[1:cha_index]
                parts = request_method_and_url_str.split(' ')
                # 空格分割，三部分为请求方法，完整请求url，请求协议/版本
                if len(parts) != 3:
                    raise ValueError('method and url parse error')
                # 请求方法
                row_info['request_method'] = parts[0] if __request_method_is_valid(
                    request_method=parts[0]) else None
                # 完整url
                row_info['request_url'] = parts[1] if __request_url_is_valid(request_url=parts[1]) else None

                # 资源类型和请求参数
                row_info.update(_parse_url_resource_type_and_params(row_info['request_url']))

                sub_parts = parts[2].split('/')
                if len(sub_parts) != 2:
                    raise ValueError('protocol/version parse error')
                row_info['request_protocol'] = sub_parts[0] \
                    if __request_protocol_is_valid(request_protocol=sub_parts[0]) else None
                row_info['request_protocol_version'] = sub_parts[1] \
                    if __request_protocol_version_is_valid(request_protocol_version=sub_parts[1]) else None

                self._parse_response_status_code(part_file_line[cha_index + 1:], row_info)
                return

        raise ValueError(f'request method/url/protocol/version parse error')

    def _parse_response_status_code(self, part_file_line, row_info):
        """6. 提取相应状态码"""

        def __response_status_code_is_valid(**kwargs):
            return True

        part_file_line = part_file_line.lstrip()
        for cha_index in range(len(part_file_line)):
            if part_file_line[cha_index] == ' ':
                response_status_code = part_file_line[:cha_index]
                row_info['response_status_code'] = response_status_code \
                    if __response_status_code_is_valid(response_status_code=response_status_code) else None

                self._parse_response_bytes(part_file_line[cha_index + 1:], row_info)
                return

        raise ValueError('response status code parse error')

    def _parse_response_bytes(self, part_file_line, row_info):
        """6. 提取相应字节数"""

        def __response_bytes_is_valid(**kwargs):
            return True

        part_file_line = part_file_line.lstrip()

        response_bytes = part_file_line
        row_info['response_bytes'] = response_bytes \
            if __response_bytes_is_valid(response_bytes=response_bytes) else None

        return

    def result(self):
        """输出解析结果"""
        return self._parse_result


if __name__ == '__main__':
    pass
