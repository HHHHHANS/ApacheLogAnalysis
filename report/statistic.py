"""内容统计模块

输入：列名
输出：相应列名的统计内容
"""
import pandas as pd
from typing import List
from report.md import MarkDownTable
from report.md import MdTableDict
from collections import OrderedDict

# 文章类型
Article_Type = ['.html', '.htm', 'html', 'htm']
# TODO 统计与解析对应键
Column_Mapper = {'url': 'request_url',
                 'res_type': 'request_resource_type',
                 'ip': 'request_ip'}

Tmp_md_local_dir = '../debug'


class BaseStatisticModule:
    """基础统计模块"""

    def __init__(self):
        pass


class ApacheLogReporter(BaseStatisticModule):
    """
    适用于Apache V.x.x.x版本的统计模块
    """
    def __init__(self):
        super(ApacheLogReporter, self).__init__()
        self._origin_report = pd.DataFrame()
        self._keys = set()

    def parser_content_2_statistic(self, content: List[dict]):
        """从解析器到统计模块的转换"""
        if not content:
            raise ValueError('empty content to transform.')

        self._origin_report = content
        self._keys = content[0].keys()

    def ip_report(self):
        """生成ip报表

        """
        ip_dict = dict()
        ip_list, visit_list, article_list = [], [], []

        for row in self._origin_report:
            ip = row[Column_Mapper['ip']]
            res_type = row[Column_Mapper['res_type']]
            if not ip:
                continue
            elif ip not in ip_dict.keys():
                ip_dict[ip] = len(ip_list)
                ip_list.append(ip)
                visit_list.append(1)
                article_list.append(1 if res_type in Article_Type else 0)
            else:
                visit_list[ip_dict[ip]] += 1
                article_list[ip_dict[ip]] += 1 if res_type in Article_Type else 0

        content_dict = MdTableDict()
        content_dict['IP'] = ip_list
        content_dict['访问次数'] = visit_list
        content_dict['访问文章数'] = article_list
        md_table = MarkDownTable()
        md_table.transform(content_dict)

        return md_table

    def article_report(self):
        """生成article(文章)报表

        """
        # TODO 获取文章标题
        tmp_title = '训练素材'
        url_list, title_list, visit_count_list, visit_ip_list = [], [], [], []
        url_2_ip = OrderedDict()
        url_dict = dict()

        for row in self._origin_report:
            url = row[Column_Mapper['url']]
            res_type = row[Column_Mapper['res_type']]
            ip = row[Column_Mapper['ip']]
            if not url or res_type not in Article_Type:
                continue
            elif url not in url_dict.keys():
                url_dict[url] = len(url_list)
                url_2_ip[url] = {ip}
                url_list.append(url)
                title_list.append(tmp_title)
                visit_count_list.append(1)
                visit_ip_list.append(1)
            else:
                visit_count_list[url_dict[url]] += 1
                if ip in url_2_ip[url]:
                    continue
                else:
                    url_2_ip[url].add(ip)
                    visit_ip_list[url_dict[url]] += 1

        content_dict = MdTableDict()
        content_dict['URL'] = url_list
        content_dict['文章标题'] = title_list
        content_dict['访问人次'] = visit_count_list
        content_dict['访问IP数'] = visit_ip_list
        md_table = MarkDownTable()
        md_table.transform(content_dict)
        # print(md_table)

        return md_table

    def complete_report(self):
        """生成完整报表

        """
        url_and_ip_dict = dict()
        url_list, ip_list, count_list = [], [], []

        for row in self._origin_report:
            url = row[Column_Mapper['url']]
            ip = row[Column_Mapper['ip']]
            u_id = url + ip
            if not url or not ip:
                continue
            if u_id not in url_and_ip_dict.keys():
                url_and_ip_dict[u_id] = len(url_list)
                url_list.append(url)
                ip_list.append(ip)
                count_list.append(1)
            else:
                count_list[url_and_ip_dict[u_id]] += 1

        content_dict = MdTableDict()
        content_dict['IP'] = ip_list
        content_dict['URL'] = url_list
        content_dict['访问次数'] = count_list
        md_table = MarkDownTable()
        md_table.transform(content_dict)
        # print(md_table)

        return md_table

    @staticmethod
    def dump_report_2_local(content: MarkDownTable, file_name):
        if not isinstance(content, MarkDownTable):
            raise TypeError(f'should input class Markdown table, {type(content)} instead')
        try:
            content.dump_to_local(file_name=f'{Tmp_md_local_dir}/{file_name}')
        except Exception as e:
            raise e






