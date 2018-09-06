"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""
import json

from collections import defaultdict
from bonjour.utils.db_helper import redis_handle


class DST:
    # TODO 目前为临时方案，后面改成从配置文件读取
    all_intent = {'weather':
                      {'intent': 'weather',
                       'slot': {'LOC':None, 'start_time': None, 'delta_time':None},
                       'state': 1},
                  'test_intent':
                      {'intent': 'test_intent',
                       'slot': {'slot1': None, 'slot2': None},
                       'state': 1}
                  }

    def __init__(self):
        self.slot_intent_map = self._slot_to_intent_map()

    def _slot_to_intent_map(self):
        slot2intent = defaultdict(list)
        for intent in self.all_intent:
            for slot in self.all_intent[intent]:
                slot2intent[slot].append(intent)
        return slot2intent

    def track(self, uid_intent_slot_dct):
        """
        对话状态追踪
        :param uid_intent_slot_dct:必须包含字段：uid, slot, intent
        :return:
        """
        uid = uid_intent_slot_dct['uid']
        slot_dct = uid_intent_slot_dct['slot']
        intent = uid_intent_slot_dct['intent']

        uid_slot = '{}.slot'.format(uid)
        uid_intent = '{}.intent'.format(uid)

        if intent:
            if intent not in self.all_intent:
                raise KeyError('识别意图-{}-不再意图集合-{}-范围内，请重新检查'.format(intent, self.all_intent))
            last_slot = json.loads(redis_handle.get(uid_slot)) if redis_handle.get(uid_slot) else {}
            intent_dct = self.all_intent[intent]
            if last_slot:
                for k in list(intent_dct['slot'].keys()):
                    if k in last_slot:
                        intent_dct['slot'][k] = last_slot[k]
            redis_handle.lpush(uid_intent, json.dumps(intent_dct))

        if slot_dct:
            last_slot = redis_handle.get(uid_slot)
            if last_slot:
                last_slot = json.loads(last_slot)
                last_slot.update(slot_dct)
            else:
                last_slot = slot_dct
            latest_slot = last_slot  #单纯为了可读性

            #40秒过期？
            redis_handle.set(uid_slot, json.dumps(latest_slot), ex=40)

            new_added_slot = list(slot_dct.keys())

            for i, item in enumerate(redis_handle.lrange(uid_intent, 0, -1)):
                item = json.loads(item)
                flag = 0
                for k in list(item['slot'].keys()):
                    if k in new_added_slot:
                        item['slot'][k] = slot_dct[k]
                        flag = 1

                if flag == 1 or item['intent'] == intent:
                    item['state'] = 1
                    redis_handle.lset(uid_intent, i, json.dumps(item))
                else:
                    item['state'] = 0
                    redis_handle.lset(uid_intent, i, json.dumps(item))

        else:
            for i, item in enumerate(redis_handle.lrange(uid_intent, 0, -1)):
                item = json.loads(item)

                if item['intent'] == intent:
                    item['state'] = 1
                    redis_handle.lset(uid_intent, i, json.dumps(item))
                else:
                    item['state'] = 0
                    redis_handle.lset(uid_intent, i, json.dumps(item))
