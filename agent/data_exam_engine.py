"""数据引擎：负责保证数据安全性/完整性/有效性校验"""


class BaseSafetyPolicy:
    """数据安全策略基础类"""

    def __init__(self, symbol):
        self._symbol = symbol

    def symbol(self):
        return self._symbol

    def check(self, data):
        pass


class JsonPolicy(BaseSafetyPolicy):
    """json格式数据校验策略类"""
    def __init__(self):
        super(JsonPolicy, self).__init__(symbol='json')

    def check(self, data):
        """校验json数据"""
        pass


class DataExaminationEngine:
    """数据校验引擎类"""
    def __init__(self):
        self._policy_map = dict()

    def register_policy(self, policy: BaseSafetyPolicy):
        """注册相应的安全策略类

        将安全策略集成到策略集合
        """
        policy_symbol = policy.symbol()
        self._policy_map.update({policy_symbol: policy})

    def exam(self, data):
        """依次应用策略集中策略进行数据检查"""
        try:
            for policy_key, policy in self._policy_map.items():
                policy.check(data)
        except Exception as e:
            raise e

