"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

import yaml


# 临时方案
with open('all_intent.yaml', encoding='utf8') as f:
    intent = yaml.load(f)
    print(intent)