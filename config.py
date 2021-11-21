"""配置类"""
import os
import json
import yaml
from common.common import Logger

Config_File_Suffix = '.yaml'
Default_cfg_path = ''


class BaseConfig:
    """配置文件 基础类"""

    def __init__(self, cfg_path: str):
        if not isinstance(cfg_path, str):
            raise TypeError(f'config path is not str, {cfg_path}')
        if not cfg_path.endswith(Config_File_Suffix):
            raise IOError(f'wrong config type: {cfg_path}, .yaml is required')
        self._file_path = cfg_path
        self._cfg_content = yaml.load(self._file_path)

    def cfg_validation(self):
        """配置文件内容检查"""
        pass

    def new_cfg(self):
        """生成默认内容的新配置文件"""
        pass


class UserConfig(BaseConfig):
    """用户可见配置类"""

    def __init__(self):
        super(UserConfig, self).__init__()


class SystemConfig(BaseConfig):
    """系统运行配置类，开发配置"""

    # TODO 配置文件类暂未完成，暂时写死
    TMP_excluded_res_type = ['.js', '.css']

    def __init__(self):
        super(SystemConfig, self).__init__(cfg_path='config/sys_config.yaml')


class User2StatisticKeyMapper:
    """用户可见键与统计模块键对照表"""
    pass
