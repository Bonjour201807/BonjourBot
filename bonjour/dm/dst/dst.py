import redis
import json
import yaml

from collections import defaultdict
from bonjour.nlu.nlu import NLU

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis_handle = redis.Redis(connection_pool=pool)


class DST:
    # TODO 目前为临时方案，后面改成从配置文件读取

    def __init__(self):
        self.intent_structure = yaml.load(open('/Users/pangyuming/Downloads/BonjourBot/data/intent/intent_structure.yaml'))
        self.nlu_handle = NLU()
        self.slot_intent_map = self._slot_to_intent_map()

    def _slot_to_intent_map(self):
        slot2intent = defaultdict(list)
        for intent in self.intent_structure:
            for slot in self.intent_structure[intent]:
                slot2intent[slot].append(intent)
        return slot2intent

    def dst(self, request):
        """
        对话状态追踪
        :param request:
        :return:
        """
        intent_slot = self.nlu_handle.nlu(request['query'])
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
            redis_handle.lpush(uid_intent, json.dumps(self.intent_structure[intent_slot['intent']]))

        new_added_slot = list(intent_slot['slot'].keys())
        for i, item in enumerate(redis_handle.lrange(uid_intent, 0, -1)):
            item = json.loads(item)
            flag = 0
            for k in list(item['slot'].keys()):
                if k in new_added_slot:
                    item['slot'][k] = intent_slot['slot'][k]
                    flag = 1

            if flag == 1:
                item['state'] = 1
                redis_handle.lset(uid_intent, i, json.dumps(item))
            else:
                item['state'] = 0
                redis_handle.lset(uid_intent, i, json.dumps(item))


