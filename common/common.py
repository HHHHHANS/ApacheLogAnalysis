""" 公共类"""
import os
import logging

Logger = logging


class LogFileNotFoundError(Exception):
    """日志文件不存在错误"""
    pass


class LogFilePathError(Exception):
    """日志文件路径错误"""
    pass


class FileTypeError(Exception):
    """文件类型错误"""
    pass