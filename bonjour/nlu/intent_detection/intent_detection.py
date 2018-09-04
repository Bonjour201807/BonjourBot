"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

import re
import os
import yaml

from bonjour.utils import Singleton


class Intent(Singleton):

    def __init__(self):
        # 临时方案,有数据情况下训练分类器
        self.rule2intent = {}
        intent_path = os.path.dirname(__file__) + '/intent.yaml'
        with open(intent_path, encoding='utf8') as f:
            intent_dict = yaml.load(f)
            intent_keys = intent_dict['intent'].keys()
            for intent in intent_keys:
                for rule_expr in intent_dict['intent'][intent]:
                    self.rule2intent[re.compile(rule_expr)] = intent

    def intent_recognition(self, query):
        # 临时方案
        intent_map = {'intent': ''}
        for rule_expr, intent_word in self.rule2intent.items():
            if rule_expr.search(query):
                intent_map['intent'] = intent_word
                return intent_map
        return intent_map


if __name__ == '__main__':
    Intent1 = Intent
    Intent2 = Intent
    print(Intent1.intent_recognition('我想出去玩'))
    print(id(Intent1))
    print(id(Intent2))
