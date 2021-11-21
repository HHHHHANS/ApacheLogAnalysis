""" markdown文本处理类"""
from typing import OrderedDict


class MdTableDict(OrderedDict):
    """可以被MarkDownTable类读取并转换为相应格式的形式"""

    def __init__(self):
        super(MdTableDict, self).__init__()

    def checked(self):
        """对字典内容做校验：
        每个key对应value为相同长度的list
        """
        last_v_size = None
        for v in self.values():
            if not isinstance(v, list):
                return False
            if last_v_size is None:
                last_v_size = len(v)
            else:
                if last_v_size != len(v):
                    return False
        return True

    def str_key(self):
        """返回字符串key列表， 主要用于str.join()"""
        keys = self.keys()
        return [str(key) for key in keys]

    def value_size(self):
        """返回第一个key对应value的长度，检查不通过则"""
        if not self.checked():
            return 0
        else:
            for k in self.keys():
                return len(self.get(k))

    def append_row(self, row: dict):
        if not self.keys():
            for k, v in row.items():
                self.__setitem__(k, [v])
        else:
            for k, v in row.items():
                if k not in self.keys():
                    raise KeyError(f'{k} is not defined')
                else:
                    self[k].append(v)


class MarkDownTable:
    """markdown表格类"""

    def __init__(self):
        self._sep_cha = '|'
        self._row_sep = '\n'
        self._table = None

    def table(self):
        return self._table

    def transform(self, content: MdTableDict):
        """读取字典格式的内容，转换成md表格形式的字符串、
        字典内容有效性由数据类型本身保证
        """

        if not isinstance(content, MdTableDict):
            raise TypeError(f'should receive \'MdTableDict\' type, {type(content)} instead.')
        if not content.checked():
            raise ValueError(f'content of MdTableDict is not valid. {content}')

        all_lines = list()
        all_lines.append(self._sep_cha + str.join(self._sep_cha, list(content.str_key())) + self._sep_cha)
        all_lines.append(self._sep_cha + str.join(self._sep_cha, ['---' for _ in range(len(content.keys()))]) + self._sep_cha)

        for i in range(content.value_size()):
            one_content_line = []
            for k in content.keys():
                one_content_line.append(str(content[k][i]))
            one_content_line = self._sep_cha + str.join(self._sep_cha, one_content_line) + self._sep_cha
            all_lines.append(one_content_line)

        self._table = str.join(self._row_sep, all_lines)

    def __repr__(self):
        """打印实例对象，返回格式转换完成的字符串"""
        return self._table

    def dump_to_local(self, file_name):
        """将报告内容保存到本地文件
        """
        if not isinstance(file_name, str):
            raise TypeError(f'should input class str of file name, {type(file_name)} instead')
        if not file_name:
            raise ValueError(f'should input non empty file name')

        if file_name.endswith('.md'):
            return self.export_md_file(file_name)

    def export_md_file(self, file_name):
        """将表格内容单独导出成 .md 文件"""
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(self._table)


if __name__ == '__main__':
    # 按列插入
    content_dict = MdTableDict()
    content_dict['a'] = [1,2,3]
    content_dict['b'] = [2,3,4]
    content_dict['c'] = [3,4,5]
    md_table = MarkDownTable()
    md_table.transform(content_dict)
    print(md_table)

    # 按行插入
    content_dict_2 = MdTableDict()
    content_dict_2.append_row({'a1': 1, 'b1': 2, 'c1': 3})
    content_dict_2.append_row({'a1': 3, 'b1': 1, 'c1': 1})
    md_table_2 = MarkDownTable()
    md_table_2.transform(content_dict_2)
    print(md_table_2)
