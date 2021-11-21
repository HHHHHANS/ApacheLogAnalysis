""" 本地数据读取模块"""
import os
from common.common import LogFileNotFoundError
from common.common import LogFilePathError
from common.common import FileTypeError


class BaseFileLoader:
    """文件读取基础类"""

    def __init__(self, file_path: str, file_suffix: str):
        self._file_suffix = file_suffix
        self._file_buffer = None
        self._buffer_lines = None
        self._read(file_path)

    def suffix(self):
        return self._file_suffix

    def _check_suffix(self, file_path: str):
        """文件格式检查"""
        if file_path.endswith(self._file_suffix):
            return True
        else:
            return False

    def _read(self, file_path: str, encoding='utf-8'):
        """读取文件资源"""
        try:
            if not self._check_suffix(file_path=file_path):
                raise FileTypeError(f'expected suffix: {self._file_suffix}, {file_path} instead')
            if not os.path.exists(file_path):
                raise FileNotFoundError(f'{file_path}')
            f = open(file_path, 'r', encoding=encoding)
            self._file_buffer = f
            self._buffer_lines = f.readlines()
        except FileNotFoundError as e:
            raise e
        except IOError as e:
            raise e
        except FileTypeError as e:
            raise e

    def close(self):
        """关闭文件资源"""
        if self._file_buffer is None:
            return
        else:
            try:
                self._file_buffer.close()
            except IOError as e:
                raise e

    def buffer_lines(self):
        return self._file_buffer

    def parse_with_parser(self, parser):
        """使用特定解析器，解析文件内容，产生报告"""
        try:
            report = parser.parse(self._buffer_lines)
        except Exception as e:
            raise e

        return report


class LogFileLoader(BaseFileLoader):
    """.log 日志文件读取类"""

    def __init__(self, file_path: str):
        self._log_suffix = '.log'
        super(LogFileLoader, self).__init__(file_path, self._log_suffix)


class TxtFileLoader(BaseFileLoader):
    """.txt 文本文件读取类"""

    def __init__(self, file_path: str):
        self._log_suffix = '.txt'
        super(TxtFileLoader, self).__init__(file_path, self._log_suffix)


if __name__ == '__main__':
    path = 'resource/example_log.log'
    log_loader = LogFileLoader(file_path=path)
