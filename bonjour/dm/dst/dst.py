"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""
import json
from collections import defaultdict

from bonjour.nlu import NLU
from bonjour.utils.db_helper import redis_handle


class DST:
    # TODO 目前为临时方案，后面改成从配置文件读取
    all_intent = {'weather':
                      {'intent': 'weather',
                       'slot': {'LOC':None, 'start_time': None, 'delta_time':None},
                       'state': 0},
                  'test_intent':
                      {'intent': 'test_intent',
                       'slot': {'slot1': None, 'slot2': None},
                       'state': 0}
                  }

    def __init__(self):
        self.nlu_handle = NLU()
        self.slot_intent_map = self._slot_to_intent_map()

    def _slot_to_intent_map(self):
        slot2intent = defaultdict(list)
        for intent in self.all_intent:
            for slot in self.all_intent[intent]:
                slot2intent[slot].append(intent)
        return slot2intent

    def dst(self, request):
        """
        对话状态追踪
        :param request:
        :return:
        """
        intent_slot = self.nlu_handle.nlu(request['query'])
        print('intent_slot...', intent_slot)
        uid = request['uid']
        uid_slot = '{}:slot'.format(uid)
        uid_intent = '{}:intent'.format(uid)

        last_slots = redis_handle.lindex(uid_slot, 0)
        if last_slots:
            last_slots = json.loads(last_slots)
            last_slots.update(intent_slot['slot'])
        else:
            last_slots = intent_slot['slot']

        latest_slots = last_slots  #单纯为了可读性
        redis_handle.lpush(uid_slot, json.dumps(latest_slots))

        if intent_slot['intent']:
            redis_handle.lpush(uid_intent, json.dumps(self.all_intent[intent_slot['intent']]))

        new_added_slot = list(intent_slot['slot'].keys())

        is_any_change = 0
        for i, item in enumerate(redis_handle.lrange(uid_intent, 0, -1)):
            print('load item',i,item)
            item = json.loads(item)
            flag = 0
            for k in list(item['slot'].keys()):
                if k in new_added_slot:
                    item['slot'][k] = intent_slot['slot'][k]
                    flag = 1

            if flag == 1 or item['intent'] == intent_slot['intent']:
                item['state'] = 1
                redis_handle.lset(uid_intent, i, json.dumps(item))
                is_any_change += 1
            else:
                item['state'] = 0
                redis_handle.lset(uid_intent, i, json.dumps(item))
        print('is_any_change: ',is_any_change)
        if is_any_change == 0:
            for i, item in enumerate(redis_handle.lrange(uid_intent, 0, -1)):
                item = json.loads(item)
                if self._has_none(item['slot']):
                    item['state'] = 1
                    redis_handle.lset(uid_intent, i, json.dumps(item))
                    break
                else:
                    continue

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



