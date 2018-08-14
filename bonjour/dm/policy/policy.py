"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

import json
import random

from bonjour.dm.dst.dst import DST, redis_handle


class Policy:
    def __init__(self):
        self.dst_handle = DST()

        # 临时方案，要改成配置文件
        self.policy_tree = {
            'weather': [
                {'LOC': [
                    '请问在哪儿呢？',
                    '请问你想问哪儿的天气'
                ]},
                {'start_time': [
                    '什么时候的呢？',
                    '你想问什么时候的天气',
                    '请告诉我查询的时间，谢谢tmd'
                ]}
            ]
        }

    def policy(self, request):
        self.dst_handle.dst(request)
        uid = request['uid']
        uid_slot = '{}:slot'.format(uid)
        uid_intent = '{}:intent'.format(uid)

        for item in redis_handle.lrange(uid_intent, 0, -1):
            item = json.loads(item)
            print('policy_item: ', item)
            if item['state'] == 1:
                is_has_none = self._has_none(item['slot'])
                # print('is_has_none...', is_has_none)
                if not is_has_none:
                    return {'answer': item,
                            'question': '',
                            'tag': 1,
                            'intent': item['intent']}
                else:
                    for slot_dct in self.policy_tree[item['intent']]:
                        for slot, questions in slot_dct.items():
                            if slot in is_has_none:
                                question = random.choice(questions)
                                return {'answer': '',
                                        'question': question,
                                        'tag': 0,
                                        'intent': item['intent']}
            else:
                continue

        return None

    def _has_none(self, dct):
        """
        检查一个字典是否有value为None
        :param dct:
        :return:
        """
        none_keys = []
        for k, v in dct.items():
            if (not v) or v == 'None':
                none_keys.append(k)
        if none_keys:
            return none_keys
        else:
            return None
