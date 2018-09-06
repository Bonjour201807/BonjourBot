"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

import json
import random

from bonjour.utils import redis_handle, has_none
from bonjour.dm.dst import DST


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

    def process(self, uid_intent_slot_dct):
        '''

        :param uid_intent_slot_dct: 必须包含字段：uid, slot, intent
        :return:
        '''

        self.dst_handle.track(uid_intent_slot_dct)
        uid = uid_intent_slot_dct['uid']
        uid_slot = '{}.slot'.format(uid)
        uid_intent = '{}.intent'.format(uid)

        for item in redis_handle.lrange(uid_intent, 0, 10):
            item = json.loads(item)
            #print('policy_item: ', item)
            if item['state'] == 1:
                is_has_none = has_none(item['slot'])
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


if __name__ == '__main__':
    plicyer = Policy()
    uid = '0001'
    print(plicyer.process({'uid': uid, 'intent': 'weather','slot':{}}))
    print(plicyer.process({'uid': uid, 'intent': '', 'slot': {'asd':'深圳','asdf':123}}))
    print(plicyer.process({'uid': uid, 'intent': '', 'slot': {}}))
    print(plicyer.process({'uid': uid, 'intent': '', 'slot': {'start_time':'明天','delta_time':'as'}}))


